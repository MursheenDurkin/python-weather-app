"""
weather_extended.py
-------------------
Fetches and displays detailed current weather for a given city.
Supports Metric (°C, m/s) and Imperial (°F, mph) units.

Displays:
    Temperature, Description, Humidity, Wind Speed,
    Pressure, Visibility, Sunrise & Sunset (city local time)

Usage:
    python3 weather_extended.py
    python3 weather_extended.py London

Setup:
    See README.md for API key configuration.

Requirements:
    pip install -r requirements.txt
"""

import os
import sys
from datetime import datetime, timezone, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

UNITS = {
    "m": {"api": "metric",   "label": "Metric",   "temp": "°C", "speed": "m/s"},
    "i": {"api": "imperial", "label": "Imperial", "temp": "°F", "speed": "mph"},
}


# ──────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────

def load_api_key() -> str:
    """
    Load the OpenWeatherMap API key from the environment.
    Exits with a helpful message if it is not set.
    """
    key = os.environ.get("OPENWEATHER_API_KEY", "").strip()
    if not key:
        print(
            "\n[Error] OPENWEATHER_API_KEY is not set.\n"
            "\n  Option 1 — create a .env file in this directory:\n"
            "    OPENWEATHER_API_KEY=your_key_here\n"
            "\n  Option 2 — export it in your shell:\n"
            "    export OPENWEATHER_API_KEY=your_key_here\n"
            "\n  Get a free key at: https://openweathermap.org/api\n"
        )
        sys.exit(1)
    return key


def prompt_units() -> str:
    """
    Ask the user to choose between metric and imperial.
    Returns 'm' or 'i'. Defaults to metric on unrecognised input.
    """
    choice = input("Choose units (m for metric, i for imperial): ").strip().lower()
    if choice == "i":
        return "i"
    if choice != "m":
        print("  Unrecognised choice — defaulting to metric.")
    return "m"


def local_time(unix_ts: int, utc_offset: int) -> str:
    """
    Convert a Unix timestamp to HH:MM:SS in the city's own timezone.

    The API returns a 'timezone' field (UTC offset in seconds) for the
    queried city, so sunrise/sunset will always show the city's local
    time regardless of where the script is being run.
    """
    utc  = datetime.fromtimestamp(unix_ts, tz=timezone.utc)
    local = utc + timedelta(seconds=utc_offset)
    return local.strftime("%H:%M:%S")


def fetch_weather(api_key: str, city: str, unit_key: str) -> dict:
    """
    Call the OpenWeatherMap API and return a cleaned weather dict.
    Raises SystemExit on any failure so the caller stays simple.
    """
    params = {
        "q":     city,
        "appid": api_key,
        "units": UNITS[unit_key]["api"],
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        sys.exit("\n[Error] No internet connection — check your network and try again.")
    except requests.exceptions.Timeout:
        sys.exit("\n[Error] Request timed out — the server may be busy, try again shortly.")
    except requests.exceptions.RequestException as exc:
        sys.exit(f"\n[Error] Unexpected request error: {exc}")

    if response.status_code == 401:
        sys.exit("\n[Error] Invalid API key — double-check OPENWEATHER_API_KEY.")
    if response.status_code == 404:
        sys.exit(f"\n[Error] City '{city}' not found — check the spelling and try again.")
    if response.status_code != 200:
        sys.exit(f"\n[Error] Unexpected server response (HTTP {response.status_code}).")

    raw        = response.json()
    utc_offset = raw.get("timezone", 0)
    visibility = raw.get("visibility", None)

    return {
        "city":        raw["name"],
        "country":     raw["sys"]["country"],
        "temperature": raw["main"]["temp"],
        "description": raw["weather"][0]["description"].capitalize(),
        "humidity":    raw["main"]["humidity"],
        "wind_speed":  raw["wind"]["speed"],
        "pressure":    raw["main"]["pressure"],
        "visibility":  f"{visibility:,} m" if isinstance(visibility, int) else "N/A",
        "sunrise":     local_time(raw["sys"]["sunrise"], utc_offset),
        "sunset":      local_time(raw["sys"]["sunset"],  utc_offset),
    }


def display_weather(weather: dict, unit_key: str) -> None:
    """Render detailed weather data as a formatted terminal box."""
    u      = UNITS[unit_key]
    header = f"  {weather['city']}, {weather['country']}  [{u['label']}]"
    width  = max(45, len(header) + 2)
    bar    = "─" * width

    print(f"\n┌{bar}┐")
    print(f"{header}")
    print(f"├{bar}┤")
    print(f"  🌡  Temperature  : {weather['temperature']}{u['temp']}")
    print(f"  🌤  Description  : {weather['description']}")
    print(f"  💧  Humidity     : {weather['humidity']}%")
    print(f"  💨  Wind Speed   : {weather['wind_speed']} {u['speed']}")
    print(f"  🔵  Pressure     : {weather['pressure']} hPa")
    print(f"  👁   Visibility   : {weather['visibility']}")
    print(f"  🌅  Sunrise      : {weather['sunrise']}  (city local time)")
    print(f"  🌇  Sunset       : {weather['sunset']}  (city local time)")
    print(f"└{bar}┘\n")


# ──────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────

def main() -> None:
    api_key = load_api_key()

    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
    else:
        city = input("Enter the city name: ").strip()

    if not city:
        sys.exit("[Error] City name cannot be empty.")

    unit_key = prompt_units()
    weather  = fetch_weather(api_key, city, unit_key)
    display_weather(weather, unit_key)


if __name__ == "__main__":
    main()
