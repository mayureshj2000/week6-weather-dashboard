# Week 6 – Weather Dashboard Application

A comprehensive **Weather Dashboard** that fetches real‑time weather data from an external API and displays it in a user‑friendly terminal interface.  
This project demonstrates API integration, external library usage, caching, and clean modular Python design.[web:78][web:82]

---

## Project Description

The application connects to the OpenWeatherMap API to retrieve:

- Current weather for any city
- 5‑day weather forecast with daily summaries
- Detailed metrics like temperature, humidity, wind, and pressure

It is built as a Python package (`weather_app`) with separate modules for configuration, API access, data parsing, and display, plus a simple interactive CLI.[web:79][web:84]

---

## What I Learned

- **API Integration**: How to authenticate with and call third‑party REST APIs (OpenWeatherMap) using query parameters and API keys.[web:79][web:80]
- **HTTP Requests**: Using the `requests` library to send GET requests, handle status codes, and deal with network errors and timeouts.[web:84]
- **JSON Processing**: Parsing nested JSON responses into clean Python dictionaries and lists that are easier to work with.[web:82]
- **Error Handling**: Managing failures such as invalid API keys, missing cities, rate limits, and network issues with clear user messages.
- **Environment Management**: Storing API keys in environment variables / `.env` instead of hard‑coding secrets in code.[web:84]
- **Package Management**: Installing and using external libraries (`requests`, `python-dotenv`, `colorama`) with `requirements.txt`.

---

## Features

-  Current weather for **any city worldwide**
-  **5‑day** weather forecast with aggregated daily highs/lows
-  Temperature unit toggle: **Celsius / Fahrenheit**
-  Weather condition icons and text descriptions (ASCII / emoji)
-  Wind speed, humidity, pressure, visibility, sunrise/sunset
-  City search with favourites (quickly re‑use saved cities)
-  Favourite cities management (add / remove / list)
-  API response **caching** on disk to reduce API calls
-  Comprehensive error handling for API and network problems
-  Export‑ready parsed data (can be easily written to CSV if extended)

## Module Responsibilities
# config.py
- Loads environment variables (especially WEATHER_API_KEY) using python-dotenv.
- Defines BASE_URL, DATA_DIR, CACHE_DIR, and FAVORITES_FILE paths.
- Ensures the data/ and data/cache/ directories exist.

# weather_api.py
- WeatherAPI class encapsulating all API communication.
- Handles:
    - Current weather (get_current_weather)
    - 5‑day forecast (get_forecast)
    - Network/HTTP error handling and status‑code based messages
    - Disk‑based JSON caching using time.time() and last‑modified times.

# weather_parser.py
- Pure functions to transform raw JSON into clean, typed dictionaries/lists:
    parse_current_weather(data, unit="C")
    parse_forecast(data, unit="C")
- Handles unit conversion (C ↔ F), date/time formatting, and daily aggregation for forecasts.

# weather_display.py
- Functions to render parsed data as a formatted CLI dashboard:
    show_current(current_data)
    show_forecast(daily_forecast)
- Uses colorama for color‑coding temperatures and simple icon mapping for common weather conditions.

# main.py
- Interactive command‑line interface:
    - Main menu (view city, favourites, manage favourites, toggle units)
    - City selection with favourites list
    - Integration of API client, parser, and display modules
- Orchestrates the full flow: get input → call API → parse → display → loop.

# tests/
- test_api.py: tests caching behaviour and API method contracts (with mock or fake data).
- test_parser.py: tests JSON parsing and conversion logic using small fake payloads.
- test_display.py: smoke tests that the display functions print expected content.
