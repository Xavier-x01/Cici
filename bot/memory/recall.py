"""
Wraps the OB1 MCP 'search' and 'recent_thoughts' tools.
Output is always Tier C — annotate before presenting to user.
Governed by users/cici/governed-state/tools/config.json.
"""
import httpx
from bot.config.settings import OB1_MCP_URL, OB1_MCP_KEY


async def search(query: str, max_results: int = 3) -> list[dict]:
    """
    Semantic search over Supabase thoughts. Returns list of thought dicts.
    Each dict has at minimum: content, metadata, created_at.
    Output trust: Tier C.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{OB1_MCP_URL}?key={OB1_MCP_KEY}",
            json={"tool": "search", "input": {"query": query, "limit": max_results}},
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", [])


async def recent_thoughts(limit: int = 5) -> list[dict]:
    """
    Retrieve the most recently captured thoughts, newest first.
    Output trust: Tier C.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            f"{OB1_MCP_URL}?key={OB1_MCP_KEY}",
            json={"tool": "recent_thoughts", "input": {"limit": limit}},
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", [])


async def build_context_for_message(user_message: str) -> str:
    """
    Retrieve top-3 memories relevant to the user's message plus top-3 preferences.
    Returns a formatted string for injection into the Claude system prompt.
    """
    relevant = await search(user_message, max_results=3)
    preferences = await search("preference", max_results=3)

    lines = []
    if preferences:
        lines.append("## Xavier's Preferences [Tier C — from memory]")
        for t in preferences:
            lines.append(f"- {t.get('content', '')}")

    if relevant:
        lines.append("## Relevant Past Context [Tier C — from memory]")
        for t in relevant:
            lines.append(f"- {t.get('content', '')}")

    return "\n".join(lines) if lines else ""
