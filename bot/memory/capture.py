"""
Wraps the OB1 MCP 'capture' tool.
Every Telegram exchange is stored in Supabase with the telegram-conversation
durability class and #telegram tag, per memory-policy governed state.
"""
import httpx
from bot.config.settings import OB1_MCP_URL, OB1_MCP_KEY


async def capture_exchange(user_message: str, cici_reply: str, extra_tags: list[str] | None = None) -> bool:
    """
    Store a conversation turn (user message + Cici reply) in Supabase.
    Durability class: telegram-conversation (30-day retention, synthesis-eligible).
    Required tags: #telegram. Additional tags may be added by caller.
    Returns True on success.
    """
    tags = ["#telegram", "#conversation"] + (extra_tags or [])
    content = f"[Telegram] User: {user_message}\nCici: {cici_reply}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{OB1_MCP_URL}?key={OB1_MCP_KEY}",
            json={
                "tool": "capture",
                "input": {
                    "content": content,
                    "durability_class": "telegram-conversation",
                    "tags": tags,
                },
            },
        )
        resp.raise_for_status()
        return True


async def capture_preference(preference_text: str) -> bool:
    """
    Store a user preference noted during a conversation.
    Durability class: persistent (90-day retention).
    Tags: #preference, #telegram.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{OB1_MCP_URL}?key={OB1_MCP_KEY}",
            json={
                "tool": "capture",
                "input": {
                    "content": preference_text,
                    "durability_class": "persistent",
                    "tags": ["#preference", "#telegram"],
                },
            },
        )
        resp.raise_for_status()
        return True


async def capture_digest_sent(digest_text: str) -> bool:
    """
    Log that a digest was sent. Durability class: telegram-conversation.
    Tags: #telegram, #digest.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{OB1_MCP_URL}?key={OB1_MCP_KEY}",
            json={
                "tool": "capture",
                "input": {
                    "content": f"[Digest sent]\n{digest_text[:500]}",
                    "durability_class": "telegram-conversation",
                    "tags": ["#telegram", "#digest"],
                },
            },
        )
        resp.raise_for_status()
        return True
