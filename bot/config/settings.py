"""
Loads all Cici bot configuration from environment variables.
Governed by users/cici/governed-state/telegram-config/config.json.
Never hardcode secrets here — this file is committed.
"""
import os
import json
from pathlib import Path

# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]

# Comma-separated list of allowed Telegram user IDs. See telegram-config/config.json.
_raw_ids = os.environ.get("TELEGRAM_ALLOWED_USER_IDS", "")
TELEGRAM_ALLOWED_USER_IDS: set[int] = (
    {int(uid.strip()) for uid in _raw_ids.split(",") if uid.strip()}
    if _raw_ids else set()
)

# Chat ID to send digest messages to. Find yours via @userinfobot.
TELEGRAM_OWNER_CHAT_ID: int = int(os.environ["TELEGRAM_OWNER_CHAT_ID"])

# ── Claude / Anthropic ────────────────────────────────────────────────────────
ANTHROPIC_API_KEY: str = os.environ["ANTHROPIC_API_KEY"]
CLAUDE_MODEL: str = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

# ── OB1 MCP Memory ────────────────────────────────────────────────────────────
OB1_MCP_URL: str = os.environ["OB1_MCP_URL"]
OB1_MCP_KEY: str = os.environ["OB1_MCP_KEY"]

# ── Real-time data ────────────────────────────────────────────────────────────
BRAVE_SEARCH_API_KEY: str = os.environ.get("BRAVE_SEARCH_API_KEY", "")
OPENWEATHER_API_KEY: str = os.environ.get("OPENWEATHER_API_KEY", "")
WEATHER_LOCATION: str = os.environ.get("WEATHER_LOCATION", "New York,US")
FINANCIAL_DATA_API_KEY: str = os.environ.get("FINANCIAL_DATA_API_KEY", "")

# ── Repo root (for reading governed docs) ─────────────────────────────────────
REPO_ROOT: Path = Path(__file__).resolve().parents[2]

# ── Governed-state paths ──────────────────────────────────────────────────────
GOVERNED_STATE_DIR: Path = REPO_ROOT / "users" / "cici" / "governed-state"
VOICE_POLICY_PATH: Path = GOVERNED_STATE_DIR / "voice" / "session-behavior.json"
IDENTITY_PATH: Path = GOVERNED_STATE_DIR / "identity" / "instance.json"
PROACTIVITY_POLICY_PATH: Path = GOVERNED_STATE_DIR / "proactivity" / "policy.json"
REALTIME_DATA_POLICY_PATH: Path = GOVERNED_STATE_DIR / "realtime-data" / "policy.json"
OPEN_LOOPS_PATH: Path = REPO_ROOT / "docs" / "companion-agent" / "brewmind-open-loops.md"
PROPOSALS_QUEUE_PATH: Path = REPO_ROOT / "proposals" / "queue"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_voice_rules() -> str:
    """Return the voice/session-behavior.json as a formatted string for the system prompt."""
    data = load_json(VOICE_POLICY_PATH)
    rules = data.get("rules", data)
    return json.dumps(rules, indent=2)


def load_identity_summary() -> str:
    """Return a brief identity summary for the system prompt."""
    data = load_json(IDENTITY_PATH)
    name = data.get("instance_id", "Cici")
    purpose = data.get("purpose", "")
    return f"You are {name}. {purpose}"
