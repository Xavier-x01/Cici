"""
Brave Search web search integration for live query answering. Output is always Tier C.
Governed by users/cici/governed-state/realtime-data/policy.json (source: brave_search).
"""
import httpx
from bot.config.settings import BRAVE_SEARCH_API_KEY

_BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"


async def search(query: str, max_results: int = 3) -> str:
    """
    Perform a live web search for the given query.
    Returns a formatted summary annotated [C].
    Returns an empty string if the API key is not configured.
    """
    if not BRAVE_SEARCH_API_KEY:
        return "[Web search unavailable: BRAVE_SEARCH_API_KEY not configured]"

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            _BRAVE_SEARCH_URL,
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": BRAVE_SEARCH_API_KEY,
            },
            params={"q": query, "count": max_results},
        )
        resp.raise_for_status()
        data = resp.json()

    web_results = data.get("web", {}).get("results", [])
    if not web_results:
        return f"[C] No web results found for: {query}"

    lines = [f"🔍 **Web search**: {query} [C]"]
    for i, result in enumerate(web_results[:max_results], 1):
        title = result.get("title", "No title")
        desc = result.get("description", "")
        url = result.get("url", "")
        lines.append(f"{i}. **{title}**\n   {desc}\n   {url}")

    return "\n\n".join(lines)
