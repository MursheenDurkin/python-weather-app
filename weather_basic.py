"""
weather_basic.py
----------------
Fetches and displays basic current weather for a given city.
Always uses Metric units (°C, m/s).

Displays:
    Temperature, Description, Humidity, Wind Speed

Usage:
    python3 weather_basic.py
    python3 weather_basic.py London

Setup:
    See README.md for API key configuration.

Requirements:
    pip install -r requirements.txt
"""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


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


def fetch_weather(api_key: str, city: str) -> dict:
    """
    Call the OpenWeatherMap API and return a cleaned weather dict.
    Raises SystemExit on any failure so the caller stays simple.
    """
    params = {
        "q":     city,
        "appid": api_key,
        "units": "metric",
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

    raw = response.json()

    return {
        "city":        raw["name"],
        "country":     raw["sys"]["country"],
        "temperature": raw["main"]["temp"],
        "description": raw["weather"][0]["description"].capitalize(),
        "humidity":    raw["main"]["humidity"],
        "wind_speed":  raw["wind"]["speed"],
    }


def display_weather(weather: dict) -> None:
    """Render weather data as a formatted terminal box."""
    header = f"  {weather['city']}, {weather['country']}"
    width  = max(35, len(header) + 2)
    bar    = "─" * width

    print(f"\n┌{bar}┐")
    print(f"{header}")
    print(f"├{bar}┤")
    print(f"  🌡  Temperature : {weather['temperature']}°C")
    print(f"  🌤  Description : {weather['description']}")
    print(f"  💧  Humidity    : {weather['humidity']}%")
    print(f"  💨  Wind Speed  : {weather['wind_speed']} m/s")
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

    weather = fetch_weather(api_key, city)
    display_weather(weather)


if __name__ == "__main__":
    main()
