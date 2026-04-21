# Telegram Bot Setup Guide

Cici is exposed as a Telegram bot via a Supabase Edge Function (`telegram-bot`). This guide walks through the full setup from scratch.

---

## Step 1 — Create the Bot with BotFather

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a display name (e.g. `Cici`) and a username (e.g. `cici_xavier_bot`)
4. BotFather gives you a **bot token** — copy it, you'll need it in Step 3

Optional (recommended):
- `/setdescription` — short bio shown on the bot's profile
- `/setcommands` — register commands for the Telegram UI:

```
start - Start and show help
capture - Save a thought to memory
search - Search your memories
recent - Show recent thoughts
stats - Memory statistics
help - Show help
```

---

## Step 2 — Find Your Telegram User ID

You need your Telegram user ID to restrict the bot to only you.

1. Message **@userinfobot** on Telegram
2. It replies with your user ID (a number like `123456789`)
3. Keep this for Step 3

---

## Step 3 — Set Supabase Secrets

Run these commands from your terminal (Supabase CLI must be installed and linked):

```bash
# Bot token from BotFather
supabase secrets set TELEGRAM_BOT_TOKEN=<your-bot-token>

# A random secret to secure the webhook (generate one)
openssl rand -hex 16
supabase secrets set TELEGRAM_WEBHOOK_SECRET=<generated-secret>

# Anthropic API key for Claude responses
supabase secrets set ANTHROPIC_API_KEY=<your-anthropic-key>

# Your Telegram user ID (from Step 2) — restricts bot access to you only
supabase secrets set ALLOWED_TELEGRAM_USER_IDS=<your-user-id>
```

The following secrets are already set from the Open Brain MCP setup and are reused automatically:
- `MCP_ACCESS_KEY` — used to call the open-brain-mcp memory function
- `SUPABASE_URL` — auto-injected by Supabase Edge Functions runtime

---

## Step 4 — Deploy the Edge Function

```bash
supabase functions deploy telegram-bot --no-verify-jwt
```

After deploy, note your function URL:
```
https://<YOUR_PROJECT_REF>.supabase.co/functions/v1/telegram-bot
```

---

## Step 5 — Register the Webhook with Telegram

Tell Telegram where to deliver updates (replace placeholders):

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://<YOUR_PROJECT_REF>.supabase.co/functions/v1/telegram-bot",
    "secret_token": "<YOUR_TELEGRAM_WEBHOOK_SECRET>"
  }'
```

Verify the webhook is set:

```bash
curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

You should see `"url"` set to your function URL and `"pending_update_count": 0`.

---

## Step 6 — Test the Bot

Open Telegram, find your bot by username, and send `/start`.

You should see the welcome message. Then try:

```
/capture Testing my Cici bot setup
/search bot setup
/recent
Hello, Cici! What can you help me with?
```

---

## Available Commands

| Command | Description |
|---|---|
| `/start` | Welcome message and command list |
| `/help` | Show commands |
| `/capture <text>` | Save a thought to Open Brain memory |
| `/search <query>` | Search your memories |
| `/recent` | Show 5 most recent thoughts |
| `/stats` | Memory statistics |
| (any message) | Chat with Cici via Claude |

---

## Secrets Reference

| Secret | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Yes | From BotFather |
| `TELEGRAM_WEBHOOK_SECRET` | Recommended | Secures the webhook endpoint |
| `ANTHROPIC_API_KEY` | Yes | For Claude AI chat responses |
| `ALLOWED_TELEGRAM_USER_IDS` | Recommended | Comma-separated user IDs; restricts access |
| `MCP_ACCESS_KEY` | Already set | Reused from Open Brain MCP setup |
| `SUPABASE_URL` | Auto | Injected by Supabase runtime |

---

## Redeployment

After code changes:

```bash
supabase functions deploy telegram-bot --no-verify-jwt
```

No need to re-register the webhook — it stays pointed at the same URL.

---

## Rotating Secrets

```bash
# Rotate bot token (also requires re-registering the webhook URL)
supabase secrets set TELEGRAM_BOT_TOKEN=<new-token>

# Rotate webhook secret (also requires re-registering via setWebhook)
openssl rand -hex 16
supabase secrets set TELEGRAM_WEBHOOK_SECRET=<new-secret>
```

---

## Troubleshooting

| Issue | Check |
|---|---|
| Bot doesn't respond | Verify webhook with `getWebhookInfo`; check Supabase function logs |
| "Unauthorized" in response | Your user ID isn't in `ALLOWED_TELEGRAM_USER_IDS` |
| Memory commands fail silently | Verify `MCP_ACCESS_KEY` is set and open-brain-mcp is deployed |
| Chat responses fail | Verify `ANTHROPIC_API_KEY` is set and valid |
| Webhook returns 401 | `TELEGRAM_WEBHOOK_SECRET` mismatch between Supabase secret and `setWebhook` call |

View function logs:

```bash
supabase functions logs telegram-bot --tail
```
