# 🌤 Python Weather App

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![OpenWeatherMap](https://img.shields.io/badge/OpenWeatherMap-API-orange?style=for-the-badge&logo=OpenWeatherMap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

A command-line weather app built in Python. Type in a city, get the current weather — simple as that. Built as one of my first Python projects while learning the basics of APIs, `requests`, and version control with Git.

---

## 📦 Scripts

| File | Description |
|------|-------------|
| `weather_basic.py` | Basic weather — temperature, description, humidity & wind speed |
| `weather_extended.py` | Extended weather — everything above plus pressure, visibility, sunrise & sunset. Supports Metric & Imperial! |

---

## 🖥️ Example Output

**weather_basic.py**
```
Enter the city name: Belfast

┌──────────────────────────────────────┐
  Belfast, GB
├──────────────────────────────────────┤
  🌡  Temperature : 1.88°C
  🌤  Description : Scattered clouds
  💧  Humidity    : 88%
  💨  Wind Speed  : 1.54 m/s
└──────────────────────────────────────┘
```

**weather_extended.py** (Metric)
```
Enter the city name: Swansea
Choose units (m for metric, i for imperial): m

┌──────────────────────────────────────────────┐
  Swansea, GB  [Metric]
├──────────────────────────────────────────────┤
  🌡  Temperature  : 3.21°C
  🌤  Description  : Light rain
  💧  Humidity     : 79%
  💨  Wind Speed   : 1.79 m/s
  🔵  Pressure     : 997 hPa
  👁   Visibility   : 10,000 m
  🌅  Sunrise      : 08:20:39  (city local time)
  🌇  Sunset       : 16:22:14  (city local time)
└──────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/MursheenDurkin/python-weather-app.git
cd python-weather-app
```

### 2. (Recommended) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key 🔐

This app uses the [OpenWeatherMap API](https://openweathermap.org/api). The free tier is more than enough.

1. Create a free account at [openweathermap.org](https://openweathermap.org/)
2. Go to **API Keys** in your dashboard and copy your key
3. Create a `.env` file in the project root:

```
OPENWEATHER_API_KEY=your_key_here
```

> ⚠️ Never commit your `.env` file — it's already listed in `.gitignore` so you're covered.

> ⏳ New keys can take up to 10 minutes to activate after creation.

### 5. Run it

```bash
# Basic version
python3 weather_basic.py

# Extended version
python3 weather_extended.py

# You can also pass the city directly as an argument
python3 weather_basic.py Belfast
python3 weather_extended.py New York
```

---

## 📁 Project Structure

```
├── weather_basic.py      # Basic weather script
├── weather_extended.py   # Extended weather script with unit choice
├── requirements.txt      # Python dependencies
├── .env                  # Your API key (not committed — see .gitignore)
├── .gitignore            # Ignores .env, __pycache__, venv, etc.
└── README.md
```

---

## 🛠️ Built With

- [Python 3](https://www.python.org/)
- [requests](https://pypi.org/project/requests/) — HTTP calls to the weather API
- [python-dotenv](https://pypi.org/project/python-dotenv/) — loads API key from `.env`
- [OpenWeatherMap API](https://openweathermap.org/api) — weather data source

---

## 📋 Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`
- A free OpenWeatherMap API key

---

## 🙋 About

This was one of my first Python projects — built while getting to grips with APIs, the `requests` library, and using Git/GitHub for version control. It's been cleaned up since the original version with better error handling, secure API key management, and proper project structure.

---

*Made with ☕ and a lot of trial and error*
