"""
Daily digest handler. Composes and sends the morning digest to Xavier.
Governed by users/cici/governed-state/proactivity/policy.json.
Scheduled via APScheduler; can also be triggered manually with /digest.
"""
import logging
from datetime import datetime, timezone
from telegram import Bot
from telegram.ext import ContextTypes, Application

from bot.config.settings import TELEGRAM_OWNER_CHAT_ID, load_json, PROACTIVITY_POLICY_PATH
from bot.integrations.weather import get_current_weather
from bot.integrations.news import get_top_headlines
from bot.integrations.brewmind import get_open_loops, get_pending_proposals, get_brewmind_status
from bot.memory.capture import capture_digest_sent

logger = logging.getLogger(__name__)

_DIGEST_PAUSED: set[int] = set()


def is_paused(chat_id: int) -> bool:
    return chat_id in _DIGEST_PAUSED


def pause_digest(chat_id: int) -> None:
    _DIGEST_PAUSED.add(chat_id)


def resume_digest(chat_id: int) -> None:
    _DIGEST_PAUSED.discard(chat_id)


async def compose_digest() -> str:
    """
    Build the full digest string from all enabled sections in the proactivity policy.
    Each section is independently fault-tolerant — a failed API call produces an empty section.
    """
    policy = load_json(PROACTIVITY_POLICY_PATH)
    digest_config = policy.get("digest", {})
    sections_config = {s["id"]: s for s in digest_config.get("sections", [])}
    formatting = digest_config.get("formatting", {})
    separator = formatting.get("section_separator", "\n\n---\n\n")
    header_template = formatting.get("header", "Good morning! Here's your digest for {date}.")
    max_chars = formatting.get("max_total_chars", 3500)

    today = datetime.now(timezone.utc).strftime("%A, %B %-d, %Y")
    header = header_template.format(date=today)

    parts = [header]

    section_order = [s["id"] for s in digest_config.get("sections", [])]
    for section_id in section_order:
        cfg = sections_config.get(section_id, {})
        if not cfg.get("enabled", True):
            continue

        try:
            content = await _fetch_section(section_id)
        except Exception as e:
            logger.warning("Digest section %s failed: %s", section_id, e)
            content = ""

        if content:
            parts.append(content)

    full = separator.join(parts)

    if len(full) > max_chars:
        full = full[:max_chars] + "\n\n_(digest truncated)_"

    return full


async def _fetch_section(section_id: str) -> str:
    if section_id == "open_loops":
        return get_open_loops()
    if section_id == "weather":
        return await get_current_weather()
    if section_id == "news_headlines":
        return await get_top_headlines()
    if section_id == "brewmind_status":
        return get_brewmind_status()
    if section_id == "pending_proposals":
        return get_pending_proposals()
    return ""


async def send_digest(bot: Bot) -> None:
    """Compose and deliver the digest to Xavier's chat. Called by APScheduler."""
    if is_paused(TELEGRAM_OWNER_CHAT_ID):
        logger.info("Digest paused for chat %s — skipping.", TELEGRAM_OWNER_CHAT_ID)
        return

    digest = await compose_digest()

    try:
        await bot.send_message(
            chat_id=TELEGRAM_OWNER_CHAT_ID,
            text=digest,
            parse_mode="Markdown",
        )
        await capture_digest_sent(digest)
        logger.info("Digest sent successfully.")
    except Exception as e:
        logger.error("Failed to send digest: %s", e)


async def handle_digest_command(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Telegram /digest command: resume digest and send one immediately."""
    chat_id = update.effective_chat.id
    resume_digest(chat_id)
    digest = await compose_digest()
    for chunk in _split_message(digest):
        await update.message.reply_text(chunk, parse_mode="Markdown")


async def handle_nodigest_command(update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Telegram /nodigest command: pause the daily digest."""
    chat_id = update.effective_chat.id
    pause_digest(chat_id)
    await update.message.reply_text(
        "Daily digest paused. Send /digest to resume or trigger one now."
    )


def _split_message(text: str, limit: int = 4000) -> list[str]:
    if len(text) <= limit:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:limit])
        text = text[limit:]
    return chunks
