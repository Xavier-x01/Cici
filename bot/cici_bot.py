"""
Cici Telegram Bot — entry point.
Registers all handlers, schedules the daily digest, and starts polling.

Run from the repo root:
    cd /path/to/Cici
    pip install -r bot/requirements.txt
    cp bot/.env.example bot/.env   # fill in your secrets
    python -m bot.cici_bot
"""
import asyncio
import logging
from datetime import time as dtime

from dotenv import load_dotenv
load_dotenv("bot/.env")  # loads before settings import

from telegram import BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.config.settings import (
    TELEGRAM_BOT_TOKEN,
    load_json,
    PROACTIVITY_POLICY_PATH,
)
from bot.handlers.message_handler import (
    handle_message,
    handle_memory_command,
)
from bot.handlers.digest_handler import (
    handle_digest_command,
    handle_nodigest_command,
    send_digest,
)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def _parse_cron(cron_str: str) -> dict:
    """Parse a 5-field cron string into APScheduler kwargs."""
    minute, hour, day, month, day_of_week = cron_str.split()
    return {
        "minute": minute,
        "hour": hour,
        "day": day,
        "month": month,
        "day_of_week": day_of_week,
    }


async def _register_commands(app: Application) -> None:
    await app.bot.set_my_commands([
        BotCommand("start", "Start a conversation with Cici"),
        BotCommand("help", "Show available commands"),
        BotCommand("memory", "Show recent memories Cici has about you"),
        BotCommand("digest", "Trigger or resume the daily digest"),
        BotCommand("nodigest", "Pause the daily digest"),
    ])


async def _start_command(update, context):
    await update.message.reply_text(
        "Hi, I'm Cici — your personal AI assistant. "
        "I remember context across our conversations and send you a morning digest. "
        "Just send me a message to get started, or use /help."
    )


async def _help_command(update, context):
    await update.message.reply_text(
        "*Cici Commands*\n"
        "/start — Start a conversation\n"
        "/memory — See recent memories\n"
        "/digest — Get today's digest now\n"
        "/nodigest — Pause the daily digest\n"
        "/help — Show this message",
        parse_mode="Markdown",
    )


def main() -> None:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # ── Command handlers ─────────────────────────────────────────────────────
    app.add_handler(CommandHandler("start", _start_command))
    app.add_handler(CommandHandler("help", _help_command))
    app.add_handler(CommandHandler("memory", handle_memory_command))
    app.add_handler(CommandHandler("digest", handle_digest_command))
    app.add_handler(CommandHandler("nodigest", handle_nodigest_command))

    # ── Message handler (catches all non-command text) ───────────────────────
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ── Daily digest scheduler ───────────────────────────────────────────────
    policy = load_json(PROACTIVITY_POLICY_PATH)
    digest_cfg = policy.get("digest", {})
    cron_str = digest_cfg.get("schedule_cron", "0 8 * * *")
    timezone_str = digest_cfg.get("timezone", "America/New_York")
    digest_enabled = digest_cfg.get("enabled", True)

    scheduler = AsyncIOScheduler(timezone=timezone_str)
    if digest_enabled:
        cron_kwargs = _parse_cron(cron_str)
        scheduler.add_job(
            send_digest,
            trigger="cron",
            kwargs={"bot": app.bot},
            **cron_kwargs,
        )
        logger.info("Digest scheduled: %s (%s)", cron_str, timezone_str)

    app.post_init = lambda a: _register_commands(a)

    scheduler.start()
    logger.info("Cici bot starting (polling mode)...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
