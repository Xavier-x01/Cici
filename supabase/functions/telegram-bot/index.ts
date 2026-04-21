import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

// ── Env ──────────────────────────────────────────────────────────────────────
const TELEGRAM_BOT_TOKEN = Deno.env.get("TELEGRAM_BOT_TOKEN") ?? "";
const TELEGRAM_WEBHOOK_SECRET = Deno.env.get("TELEGRAM_WEBHOOK_SECRET") ?? "";
const ANTHROPIC_API_KEY = Deno.env.get("ANTHROPIC_API_KEY") ?? "";
const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
const MCP_ACCESS_KEY = Deno.env.get("MCP_ACCESS_KEY") ?? "";

// Comma-separated list of allowed Telegram user IDs (leave empty to allow all)
const ALLOWED_USER_IDS: Set<number> = new Set(
  (Deno.env.get("ALLOWED_TELEGRAM_USER_IDS") ?? "")
    .split(",")
    .map((s) => parseInt(s.trim(), 10))
    .filter((n) => !isNaN(n)),
);

const TELEGRAM_API = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}`;
const MCP_ENDPOINT = `${SUPABASE_URL}/functions/v1/open-brain-mcp?key=${MCP_ACCESS_KEY}`;

const CICI_SYSTEM = `You are Cici, Xavier's personal AI assistant reachable via Telegram. You are concise, direct, and thoughtful. You have access to a persistent memory system (Xavier's Open Brain) via slash commands, but for regular conversation you rely on your training and context.

Format responses for Telegram: plain readable text, under 800 characters when possible. Avoid heavy markdown; use simple line breaks for structure.`;

// ── Telegram helpers ──────────────────────────────────────────────────────────

async function sendMessage(chatId: number, text: string): Promise<void> {
  const resp = await fetch(`${TELEGRAM_API}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, text }),
  });
  const body = await resp.json();
  console.log("sendMessage status:", resp.status, JSON.stringify(body));
}

async function sendTyping(chatId: number): Promise<void> {
  await fetch(`${TELEGRAM_API}/sendChatAction`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chatId, action: "typing" }),
  });
}

// ── MCP (Open Brain) helpers ──────────────────────────────────────────────────

async function mcpCall(
  tool: string,
  args: Record<string, unknown>,
): Promise<Record<string, unknown> | null> {
  if (!SUPABASE_URL || !MCP_ACCESS_KEY) return null;
  try {
    const resp = await fetch(MCP_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        jsonrpc: "2.0",
        method: "tools/call",
        params: { name: tool, arguments: args },
        id: 1,
      }),
    });
    if (!resp.ok) return null;
    const data = await resp.json();
    return (data.result as Record<string, unknown>) ?? null;
  } catch {
    return null;
  }
}

// ── Claude helper ─────────────────────────────────────────────────────────────

async function fetchMemoryContext(query: string): Promise<string> {
  const result = await mcpCall("search", { query, limit: 5 });
  const results = result?.results as Array<Record<string, string>> | undefined;
  if (!results?.length) return "";
  return results.map((r) => r.content ?? "").filter(Boolean).join("\n---\n");
}

async function askClaude(userMessage: string): Promise<string> {
  const memoryContext = await fetchMemoryContext(userMessage);
  const systemPrompt = memoryContext
    ? `${CICI_SYSTEM}\n\nRelevant memory context for this message:\n${memoryContext}`
    : CICI_SYSTEM;

  const resp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: "claude-opus-4-7",
      max_tokens: 1024,
      system: systemPrompt,
      messages: [{ role: "user", content: userMessage }],
    }),
  });
  if (!resp.ok) throw new Error(`Anthropic API ${resp.status}`);
  const data = await resp.json();
  return (data.content as Array<{ text: string }>)[0].text;
}

// ── Command handlers ──────────────────────────────────────────────────────────

async function cmdCapture(chatId: number, content: string): Promise<void> {
  const result = await mcpCall("capture", { content });
  if (result) {
    await sendMessage(chatId, `Saved to memory.`);
  } else {
    await sendMessage(chatId, `Memory system unavailable — could not save.`);
  }
}

async function cmdSearch(chatId: number, query: string): Promise<void> {
  const result = await mcpCall("search", { query, limit: 5 });
  const results = result?.results as Array<Record<string, string>> | undefined;
  if (!results?.length) {
    await sendMessage(chatId, `No results for: "${query}"`);
    return;
  }
  const lines = results
    .slice(0, 5)
    .map((r, i) => `${i + 1}. ${(r.content ?? "").substring(0, 120)}`)
    .join("\n\n");
  await sendMessage(chatId, `Results for "${query}":\n\n${lines}`);
}

async function cmdRecent(chatId: number): Promise<void> {
  const result = await mcpCall("recent_thoughts", { limit: 5 });
  const thoughts = result?.thoughts as Array<Record<string, string>> | undefined;
  if (!thoughts?.length) {
    await sendMessage(chatId, "No recent thoughts found.");
    return;
  }
  const lines = thoughts
    .map((t, i) => `${i + 1}. ${(t.content ?? "").substring(0, 120)}`)
    .join("\n\n");
  await sendMessage(chatId, `Recent thoughts:\n\n${lines}`);
}

async function cmdStats(chatId: number): Promise<void> {
  const result = await mcpCall("stats", {});
  if (!result) {
    await sendMessage(chatId, "Memory system unavailable.");
    return;
  }
  const lines = Object.entries(result)
    .map(([k, v]) => `${k}: ${v}`)
    .join("\n");
  await sendMessage(chatId, `Memory stats:\n${lines}`);
}

// ── Message router ────────────────────────────────────────────────────────────

async function handleMessage(message: Record<string, unknown>): Promise<void> {
  const chat = message.chat as Record<string, unknown>;
  const from = message.from as Record<string, unknown> | undefined;
  const chatId = chat?.id as number;
  const userId = from?.id as number | undefined;
  const text = (message.text as string) ?? "";

  if (!chatId || !text) return;

  // Access control: reject if user not in allowlist (when allowlist is configured)
  if (ALLOWED_USER_IDS.size > 0 && userId !== undefined && !ALLOWED_USER_IDS.has(userId)) {
    await sendMessage(chatId, "Unauthorized.");
    return;
  }

  await sendTyping(chatId);

  if (text.startsWith("/")) {
    const spaceIdx = text.indexOf(" ");
    const command = (spaceIdx === -1 ? text : text.slice(0, spaceIdx)).toLowerCase();
    const args = spaceIdx === -1 ? "" : text.slice(spaceIdx + 1).trim();

    switch (command) {
      case "/start":
        await sendMessage(
          chatId,
          "Hi, I'm Cici — Xavier's personal AI assistant.\n\n" +
            "Commands:\n" +
            "/capture <text> — save a thought to memory\n" +
            "/search <query> — search memories\n" +
            "/recent — show recent thoughts\n" +
            "/stats — memory statistics\n" +
            "/help — show this message\n\n" +
            "Send me any message to chat.",
        );
        break;

      case "/help":
        await sendMessage(
          chatId,
          "/capture <text> — save a thought\n" +
            "/search <query> — search memories\n" +
            "/recent — recent thoughts\n" +
            "/stats — memory stats\n\n" +
            "Send any message to chat with me.",
        );
        break;

      case "/capture":
        if (!args) {
          await sendMessage(chatId, "Usage: /capture <your thought>");
          break;
        }
        await cmdCapture(chatId, args);
        break;

      case "/search":
        if (!args) {
          await sendMessage(chatId, "Usage: /search <query>");
          break;
        }
        await cmdSearch(chatId, args);
        break;

      case "/recent":
        await cmdRecent(chatId);
        break;

      case "/stats":
        await cmdStats(chatId);
        break;

      default:
        await sendMessage(chatId, "Unknown command. Send /help for the list.");
    }
    return;
  }

  // General message → Claude
  try {
    const reply = await askClaude(text);
    await sendMessage(chatId, reply);
  } catch (err) {
    console.error("Claude error:", err);
    await sendMessage(chatId, "Error processing your message. Please try again.");
  }
}

// ── Webhook entry point ───────────────────────────────────────────────────────

serve(async (req) => {
  // Verify Telegram webhook secret token
  if (TELEGRAM_WEBHOOK_SECRET) {
    const token = req.headers.get("x-telegram-bot-api-secret-token");
    if (token !== TELEGRAM_WEBHOOK_SECRET) {
      return new Response("Unauthorized", { status: 401 });
    }
  }

  if (req.method !== "POST") return new Response("OK");

  try {
    const update = await req.json();
    if (update.message) await handleMessage(update.message as Record<string, unknown>);
    return new Response("OK");
  } catch (err) {
    console.error("Webhook error:", err);
    return new Response("Error", { status: 500 });
  }
});
