"""
Alpha Vantage financial/market data integration. Output is always Tier C.
Governed by users/cici/governed-state/realtime-data/policy.json (source: alpha_vantage).
Disabled by default — enabled when FINANCIAL_DATA_API_KEY is set.
"""
import httpx
from bot.config.settings import FINANCIAL_DATA_API_KEY

_BASE = "https://www.alphavantage.co/query"


async def get_quote(symbol: str) -> str:
    """
    Fetch a real-time stock or crypto quote.
    Returns a formatted string annotated [C].
    Returns a disabled notice if not configured.
    """
    if not FINANCIAL_DATA_API_KEY:
        return "[Financial data not configured: set FINANCIAL_DATA_API_KEY to enable]"

    async with httpx.AsyncClient(timeout=8.0) as client:
        resp = await client.get(
            _BASE,
            params={
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": FINANCIAL_DATA_API_KEY,
            },
        )
        resp.raise_for_status()
        data = resp.json()

    quote = data.get("Global Quote", {})
    if not quote:
        return f"[C] No quote data for {symbol}"

    price = quote.get("05. price", "N/A")
    change = quote.get("09. change", "N/A")
    change_pct = quote.get("10. change percent", "N/A")
    prev_close = quote.get("08. previous close", "N/A")

    direction = "▲" if float(change.replace(",", "") or 0) >= 0 else "▼"
    return (
        f"📈 **{symbol}** [C]\n"
        f"Price: ${price} {direction} {change} ({change_pct})\n"
        f"Prev close: ${prev_close}"
    )


async def get_market_summary() -> str:
    """
    Fetch quotes for a default set of market indicators.
    Returns an empty string if not configured.
    """
    if not FINANCIAL_DATA_API_KEY:
        return ""

    symbols = ["SPY", "QQQ", "BTC-USD"]
    results = []
    for symbol in symbols:
        results.append(await get_quote(symbol))
    return "\n".join(results)
