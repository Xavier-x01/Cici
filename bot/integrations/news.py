"""
Brave Search news integration. Output is always Tier C.
Governed by users/cici/governed-state/realtime-data/policy.json (source: brave_search).
"""
import httpx
from datetime import datetime, timezone
from bot.config.settings import BRAVE_SEARCH_API_KEY

_BRAVE_NEWS_URL = "https://api.search.brave.com/res/v1/news/search"


async def get_top_headlines(query: str = "BrewMind craft beer tech business", max_results: int = 3) -> str:
    """
    Fetch top news headlines via Brave News Search.
    Returns a formatted string annotated [C].
    Returns an empty string if the API key is not configured.
    """
    if not BRAVE_SEARCH_API_KEY:
        return ""

    async with httpx.AsyncClient(timeout=8.0) as client:
        resp = await client.get(
            _BRAVE_NEWS_URL,
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": BRAVE_SEARCH_API_KEY,
            },
            params={"q": query, "count": max_results, "freshness": "pd"},
        )
        resp.raise_for_status()
        data = resp.json()

    articles = data.get("results", [])
    if not articles:
        return ""

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"📰 **News** ({now}) [C]"]
    for i, article in enumerate(articles[:max_results], 1):
        title = article.get("title", "No title")
        url = article.get("url", "")
        source = article.get("meta_url", {}).get("hostname", "unknown source")
        lines.append(f"{i}. [{title}]({url}) — {source}")

    return "\n".join(lines)
