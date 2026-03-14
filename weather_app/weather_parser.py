# weather_app/weather_parser.py
import time
from datetime import datetime
from typing import Dict, Any, List

def kelvin_to_celsius(k: float) -> float:
    return k - 273.15

def c_to_f(c: float) -> float:
    return c * 9 / 5 + 32

def format_dt(timestamp: int, tz_offset: int) -> str:
    dt = datetime.utcfromtimestamp(timestamp + tz_offset)
    return dt.strftime("%Y-%m-%d %H:%M")

def parse_current_weather(data: Dict[str, Any], unit: str = "C") -> Dict[str, Any]:
    """Extract key fields from current weather JSON."""
    main = data.get("main", {})
    wind = data.get("wind", {})
    weather = data.get("weather", [{}])[0]
    sys = data.get("sys", {})
    tz = data.get("timezone", 0)
    temp_c = main.get("temp")
    feels_c = main.get("feels_like")

    if unit.upper() == "F":
        temp = c_to_f(temp_c)
        feels = c_to_f(feels_c)
        unit_symbol = "°F"
    else:
        temp = temp_c
        feels = feels_c
        unit_symbol = "°C"

    return {
        "city": data.get("name"),
        "country": sys.get("country"),
        "last_updated": format_dt(data.get("dt"), tz),
        "temp": temp,
        "feels_like": feels,
        "unit": unit_symbol,
        "description": weather.get("description", "").title(),
        "icon": weather.get("icon", ""),
        "humidity": main.get("humidity"),
        "wind_speed": wind.get("speed"),
        "pressure": main.get("pressure"),
        "visibility_km": (data.get("visibility", 0) / 1000),
        "sunrise": format_dt(sys.get("sunrise"), tz),
        "sunset": format_dt(sys.get("sunset"), tz),
        "_from_cache": data.get("_from_cache", False),
    }

def parse_forecast(data: Dict[str, Any], unit: str = "C") -> List[Dict[str, Any]]:
    """Aggregate 3h forecast list into daily summaries."""
    tz = data.get("city", {}).get("timezone", 0)
    result = {}
    for entry in data.get("list", []):
        dt_txt = entry.get("dt_txt")  # "YYYY-MM-DD HH:MM:SS"
        date_str = dt_txt.split(" ")[0]
        main = entry.get("main", {})
        weather = entry.get("weather", [{}])[0]

        temp = main.get("temp")
        if unit.upper() == "F":
            temp = c_to_f(temp)

        if date_str not in result:
            result[date_str] = {
                "date": date_str,
                "min": temp,
                "max": temp,
                "humidity": [main.get("humidity")],
                "descriptions": [weather.get("description", "").title()],
            }
        else:
            result[date_str]["min"] = min(result[date_str]["min"], temp)
            result[date_str]["max"] = max(result[date_str]["max"], temp)
            result[date_str]["humidity"].append(main.get("humidity"))
            result[date_str]["descriptions"].append(weather.get("description", "").title())

    daily = []
    for day in sorted(result.keys()):
        info = result[day]
        avg_h = sum(h for h in info["humidity"] if h is not None) / len(info["humidity"])
        # pick most frequent description
        desc = max(set(info["descriptions"]), key=info["descriptions"].count)
        daily.append({
            "date": day,
            "min": round(info["min"], 1),
            "max": round(info["max"], 1),
            "avg_humidity": round(avg_h),
            "description": desc,
        })
    return daily
