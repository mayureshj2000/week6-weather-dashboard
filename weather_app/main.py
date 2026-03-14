# weather_app/main.py
import json
from typing import List
from weather_app.config import FAVORITES_FILE
from weather_app.weather_api import WeatherAPI
import time
from weather_app.weather_parser import parse_current_weather, parse_forecast
from weather_app.weather_display import show_current, show_forecast

def load_favorites() -> List[str]:
    try:
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_favorites(favs: List[str]) -> None:
    with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
        json.dump(favs, f, indent=2)

def choose_city(favs: List[str]) -> str:
    if favs:
        print("\nFavourite Cities:")
        for i, city in enumerate(favs, start=1):
            print(f"{i}. {city}")
        print("0. Enter a new city")
        choice = input("Choose city (number): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(favs):
                return favs[idx - 1]
    city = input("Enter city name: ").strip()
    return city

def main():
    api = WeatherAPI()
    favorites = load_favorites()
    unit = "C"

    while True:
        print("\n=== WEATHER DASHBOARD ===")
        print("1. View weather for a city")
        print("2. View weather for favourite city")
        print("3. Manage favourite cities")
        print("4. Toggle units (C/F)")
        print("0. Quit")
        choice = input("Choose: ").strip()

        if choice == "1":
            city = choose_city([])
        elif choice == "2":
            city = choose_city(favorites)
        elif choice == "3":
            print("\nManage Favourites")
            print("-----------------")
            print("1. Add favourite")
            print("2. Remove favourite")
            print("3. List favourites")
            sub = input("Choose: ").strip()
            if sub == "1":
                new_city = input("City to add: ").strip()
                if new_city and new_city not in favorites:
                    favorites.append(new_city)
                    save_favorites(favorites)
                    print("Added to favourites.")
            elif sub == "2":
                if not favorites:
                    print("No favourites to remove.")
                else:
                    for i, c in enumerate(favorites, start=1):
                        print(f"{i}. {c}")
                    idx = input("Number to remove: ").strip()
                    if idx.isdigit():
                        n = int(idx)
                        if 1 <= n <= len(favorites):
                            removed = favorites.pop(n - 1)
                            save_favorites(favorites)
                            print(f"Removed {removed}.")
            elif sub == "3":
                if not favorites:
                    print("No favourites saved.")
                else:
                    print(", ".join(favorites))
            continue
        elif choice == "4":
            unit = "F" if unit == "C" else "C"
            print(f"Units set to {unit}.")
            continue
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
            continue

        if not city:
            print("City cannot be empty.")
            continue

        current_raw = api.get_current_weather(city)
        forecast_raw = api.get_forecast(city)

        if not current_raw:
            print("Could not fetch current weather.")
            continue

        current = parse_current_weather(current_raw, unit=unit)
        show_current(current)

        if forecast_raw:
            daily = parse_forecast(forecast_raw, unit=unit)
            show_forecast(daily)
        else:
            print("Could not fetch forecast.")

if __name__ == "__main__":
    main()