"""
Core conversation handler: user message → memory recall → Claude → reply → capture.
Governed by users/cici/governed-state/runtime-bridges/policy.json (telegram bridge).
Only users in TELEGRAM_ALLOWED_USER_IDS may interact.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
import anthropic

from bot.config.settings import (
    ANTHROPIC_API_KEY,
    CLAUDE_MODEL,
    TELEGRAM_ALLOWED_USER_IDS,
    load_voice_rules,
    load_identity_summary,
)
from bot.memory.recall import build_context_for_message, recent_thoughts
from bot.memory.capture import capture_exchange
from bot.integrations.web_search import search as web_search

logger = logging.getLogger(__name__)
_anthropic = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

_SEARCH_TRIGGERS = ("search", "look up", "find", "what is", "who is", "news about", "latest on")


def _is_allowed(user_id: int) -> bool:
    if not TELEGRAM_ALLOWED_USER_IDS:
        return False
    return user_id in TELEGRAM_ALLOWED_USER_IDS


def _wants_web_search(text: str) -> bool:
    lower = text.lower()
    return any(trigger in lower for trigger in _SEARCH_TRIGGERS)


def _build_system_prompt(memory_context: str, web_context: str = "") -> str:
    identity = load_identity_summary()
    voice = load_voice_rules()

    parts = [
        identity,
        "",
        "## Behavioral Rules (from governed voice surface)",
        voice,
        "",
        "## Evidence Tier Reminder",
        "Always annotate data sources: [A] = Xavier-verified, [B] = structured summary, [C] = model/live data.",
        "Never present Tier C data as confirmed fact. Supabase recall and live APIs are always Tier C.",
    ]

    if memory_context:
        parts += ["", memory_context]

    if web_context:
        parts += ["", "## Live Web Search Results [C]", web_context]

    return "\n".join(parts)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.message

    if not user or not message or not message.text:
        return

    if not _is_allowed(user.id):
        await message.reply_text("Sorry, I'm not configured to talk to you.")
        return

    user_text = message.text.strip()

    await context.bot.send_chat_action(chat_id=message.chat_id, action="typing")

    try:
        memory_ctx = await build_context_for_message(user_text)
    except Exception as e:
        logger.warning("Memory recall failed: %s", e)
        memory_ctx = ""

    web_ctx = ""
    if _wants_web_search(user_text):
        try:
            web_ctx = await web_search(user_text)
        except Exception as e:
            logger.warning("Web search failed: %s", e)

    system_prompt = _build_system_prompt(memory_ctx, web_ctx)

    try:
        response = await _anthropic.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_text}],
        )
        reply = response.content[0].text
    except Exception as e:
        logger.error("Claude API error: %s", e)
        reply = "I ran into an issue reaching my thinking layer. Please try again."

    # Split long replies to stay within Telegram's 4096-char limit
    for chunk in _split_message(reply):
        await message.reply_text(chunk, parse_mode="Markdown")

    try:
        await capture_exchange(user_text, reply)
    except Exception as e:
        logger.warning("Memory capture failed: %s", e)


async def handle_memory_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show Xavier the most recent memories Cici has."""
    user = update.effective_user
    if not user or not _is_allowed(user.id):
        return

    try:
        thoughts = await recent_thoughts(limit=5)
    except Exception as e:
        await update.message.reply_text(f"Could not retrieve memories: {e}")
        return

    if not thoughts:
        await update.message.reply_text("No memories found yet.")
        return

    lines = ["**Recent Memories** [C — Tier C, from Supabase]"]
    for t in thoughts:
        content = t.get("content", "")[:200]
        lines.append(f"• {content}")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


def _split_message(text: str, limit: int = 4000) -> list[str]:
    if len(text) <= limit:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:limit])
        text = text[limit:]
    return chunks
