"""
Cici Telegram Bot — simple chat mode.
No memory, no digest, no live data. Just Claude responses.
"""
import logging
import os
from dotenv import load_dotenv
load_dotenv("bot/.env")

from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ALLOWED_USER_IDS = {
    int(uid.strip())
    for uid in os.environ.get("TELEGRAM_ALLOWED_USER_IDS", "").split(",")
    if uid.strip()
}
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

_anthropic = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = (
    "You are Cici, a friendly and knowledgeable personal AI assistant on Telegram. "
    "You are helpful, concise, and conversational."
)


def _is_allowed(user_id: int) -> bool:
    if not ALLOWED_USER_IDS:
        return False
    return user_id in ALLOWED_USER_IDS


async def _start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi, I'm Cici — your personal AI assistant. Send me any message to get started!"
    )


async def _help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "*Cici Commands*\n"
        "/start — Start a conversation\n"
        "/help — Show this message",
        parse_mode="Markdown",
    )


async def _handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or not update.message or not update.message.text:
        return
    if not _is_allowed(user.id):
        await update.message.reply_text("Sorry, I'm not configured to talk to you.")
        return

    await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")

    try:
        response = await _anthropic.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": update.message.text}],
        )
        reply = response.content[0].text
    except Exception as e:
        logger.error("Claude API error: %s", e)
        reply = "I ran into an issue. Please try again."

    for chunk in ([reply[i:i+4000] for i in range(0, len(reply), 4000)]):
        await update.message.reply_text(chunk, parse_mode="Markdown")


async def _post_init(app: Application) -> None:
    await app.bot.set_my_commands([
        BotCommand("start", "Start a conversation with Cici"),
        BotCommand("help", "Show available commands"),
    ])


def main() -> None:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", _start))
    app.add_handler(CommandHandler("help", _help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_message))
    app.post_init = _post_init
    logger.info("Cici bot starting (simple mode)...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
