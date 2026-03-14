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

- ✓ Current weather for **any city worldwide**
- ✓ **5‑day** weather forecast with aggregated daily highs/lows
- ✓ Temperature unit toggle: **Celsius / Fahrenheit**
- ✓ Weather condition icons and text descriptions (ASCII / emoji)
- ✓ Wind speed, humidity, pressure, visibility, sunrise/sunset
- ✓ City search with favourites (quickly re‑use saved cities)
- ✓ Favourite cities management (add / remove / list)
- ✓ API response **caching** on disk to reduce API calls
- ✓ Comprehensive error handling for API and network problems
- ✓ Export‑ready parsed data (can be easily written to CSV if extended)
