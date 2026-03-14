# weather_app/weather_display.py
import time
from colorama import Fore, Style, init

init(autoreset=True)

ICON_MAP = {
    "clear": "☀️",
    "cloud": "☁️",
    "rain": "🌧️",
    "snow": "❄️",
    "storm": "⛈️",
    "mist": "🌫️",
}

def temp_color(temp_c: float) -> str:
    if temp_c <= 0:
        return Fore.CYAN
    elif temp_c <= 15:
        return Fore.BLUE
    elif temp_c <= 25:
        return Fore.GREEN
    elif temp_c <= 35:
        return Fore.YELLOW
    else:
        return Fore.RED

def pick_icon(description: str) -> str:
    d = description.lower()
    for key, icon in ICON_MAP.items():
        if key in d:
            return icon
    return "🌡️"

def show_current(current: dict) -> None:
    icon = pick_icon(current["description"])
    color = temp_color(current["temp"])
    cache_msg = "Using cached data" if current.get("_from_cache") else "Live data"

    print("\n🌤️  WEATHER DASHBOARD")
    print("=======================")
    print(f"\n📍 Location: {current['city']}, {current['country']}")
    print(f"🕐 Last Updated: {current['last_updated']} ({cache_msg})\n")
    print("Current Weather:")
    print("────────────────")
    print(f"Temperature:  {color}{current['temp']}{current['unit']}{Style.RESET_ALL} "
          f"(Feels like: {current['feels_like']}{current['unit']})")
    print(f"Conditions:   {current['description']} {icon}")
    print(f"Humidity:     {current['humidity']}%")
    print(f"Wind:         {current['wind_speed']} m/s")
    print(f"Pressure:     {current['pressure']} hPa")
    print(f"Visibility:   {current['visibility_km']} km")
    print(f"Sunrise:      {current['sunrise']}")
    print(f"Sunset:       {current['sunset']}\n")

def show_forecast(daily: list) -> None:
    print("5-Day Forecast:")
    print("───────────────")
    for day in daily[:5]:
        icon = pick_icon(day["description"])
        color_min = temp_color(day["min"])
        color_max = temp_color(day["max"])
        print(f"{day['date']}:  {icon}  "
              f"{color_max}{day['max']}°{Style.RESET_ALL} / "
              f"{color_min}{day['min']}°{Style.RESET_ALL}  "
              f"(Humidity: {day['avg_humidity']}%)")
    print()
