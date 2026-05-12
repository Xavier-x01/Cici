# Task 2 — Connect Your AI Client

**Phase:** 1 — Personal OB1  
**Prerequisite:** Task 1 complete (your OB1 endpoint is live and you have your MCP connection URL)  
**Estimated time:** 15–30 minutes

---

## Goal

Get your AI client (Claude, Cursor, or ChatGPT) talking to your personal OB1 instance through the MCP protocol. By the end of this task, you will have all four OB1 tools available inside your AI tool of choice.

---

## Steps

### Step 1 — Find your MCP connection URL

You built this at the end of Task 1. It looks like:

```
https://<your-project-ref>.supabase.co/functions/v1/open-brain-mcp?key=<your-mcp-access-key>
```

If you lost it, check your Supabase project settings (Project Settings → API → Project URL) and combine it with your MCP access key.

### Step 2 — Add OB1 to your AI client

**Claude (claude.ai or Claude Code CLI):**

Add to your MCP settings:
```json
{
  "mcpServers": {
    "open-brain-mcp": {
      "type": "url",
      "url": "https://<your-project-ref>.supabase.co/functions/v1/open-brain-mcp?key=<your-key>"
    }
  }
}
```

In Claude Code CLI, this goes in `~/.claude/settings.json` under `"mcpServers"`.

**Cursor:**

Go to Settings → MCP → Add Server → paste your URL. Name it `open-brain-mcp`.

**ChatGPT (with MCP plugins):**

Follow the ChatGPT plugin/tool setup for MCP-over-HTTP and paste the URL.

### Step 3 — Test all four tools

Ask your AI client to run each tool and confirm it responds:

1. `stats` — should return total thought count and date range
2. `recent_thoughts` — should return your last few stored thoughts
3. `capture` — ask Claude to capture: "Task 2 of cici-ai cohort complete."
4. `search` — ask Claude to search for "task" — should find the entry you just captured

---

## Proof

Screenshot showing:
- Your AI client open
- At least one OB1 tool call visible (e.g., `capture` or `stats` with a response)

**Option A — Telegram:** Post the screenshot in the group with your name + "Task 2 done."

**Option B — GitHub:** Create `proof/task-02/README.md` in your fork:
```
OB1 tools confirmed active in [Claude/Cursor/ChatGPT] on YYYY-MM-DD. All four tools tested.
```

---

## Stuck?

- Make sure your Edge Function is still deployed: test your URL in a browser — it should return a JSON response, not a 404.
- If the MCP server shows in your client but tools don't load, try restarting the client.
- Ask in the group — don't go silent. Others may have hit the same issue.
