"""
OpenWeatherMap integration. Output is always Tier C.
Governed by users/cici/governed-state/realtime-data/policy.json (source: openweathermap).
"""
import httpx
from datetime import datetime, timezone
from bot.config.settings import OPENWEATHER_API_KEY, WEATHER_LOCATION

_BASE = "https://api.openweathermap.org/data/2.5"


async def get_current_weather() -> str:
    """
    Fetch current weather and today's high/low for WEATHER_LOCATION.
    Returns a formatted string annotated [C].
    Returns an empty string if the API key is not configured.
    """
    if not OPENWEATHER_API_KEY:
        return ""

    async with httpx.AsyncClient(timeout=8.0) as client:
        resp = await client.get(
            f"{_BASE}/weather",
            params={
                "q": WEATHER_LOCATION,
                "appid": OPENWEATHER_API_KEY,
                "units": "imperial",
            },
        )
        resp.raise_for_status()
        data = resp.json()

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"].capitalize()
    high = data["main"]["temp_max"]
    low = data["main"]["temp_min"]
    city = data.get("name", WEATHER_LOCATION)

    now = datetime.now(timezone.utc).strftime("%H:%M UTC")
    return (
        f"🌤 **Weather** — {city} [C]\n"
        f"{desc}, {temp:.0f}°F (feels like {feels:.0f}°F)\n"
        f"High {high:.0f}°F / Low {low:.0f}°F — as of {now}"
    )
