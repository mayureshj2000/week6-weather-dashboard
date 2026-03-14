import requests
import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from .config import API_KEY, BASE_URL, CACHE_DIR

class WeatherAPI:
        """Handles all weather API interactions (current + forecast)"""
        def __init__(self, api_key: str = API_KEY, base_url: str = BASE_URL):
                self.api_key = api_key
                self.base_url = base_url
                self.cache_dir = CACHE_DIR
                self.cache_dir.mkdir(parents=True, exist_ok=True)
                self.cache_duration = 600

        def _get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
                cache_file = self.cache_dir / f"{cache_key}.json"
                if cache_file.exists():
                    cache_time = cache_file.stat().st_mtime
                    if time.time() - cache_time < self.cache_duration:
                        try:
                            with open(cache_file, "r", encoding="utf-8") as f:
                                return json.load(f)
                        except Exception:
                            return None
                return None
            
        def _save_to_cache(self, cache_key: str, data: Dict[str, Any]) -> None:
                cache_file = self.cache_dir / f"{cache_key}.json"
                try:
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                except Exception:
                    pass
        
        def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
            if not self.api_key:
                print("Error: WEATHER_API_KEY is not set in environment.")
                return None
            
            try:
                params["appid"] = self.api_key
                params["units"] = "metric"
                response = requests.get(f"{self.base_url}/{endpoint}", params=params, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    print("Error: Invalid API key.")
                elif response.status_code == 404:
                    print("Error: City  not found.")
                elif response.status_code == 429:
                    print("Error: API rate limit exceeded.")
                else:
                    print(f"Error: API request failed with status {response.status_code}.")
            except requests.exceptions.Timeout:
                print("Error: API request timed out.")
            except requests.exceptions.ConnectionError:
                print("Error: Network connection error.")
            except Exception as e:
                print(f"Error: {e}")
            return None
        
        def get_current_weather(self, city: str, country_code: str | None = None) -> Optional[Dict[str, Any]]:
            cache_key = f"current_{city}_{country_code}" if country_code else f"current_{city}"
            cached = self._get_cached_data(cache_key)
            if cached:
                cached["_from_cache"] = True
                return cached
            
            query = f"{city}, {country_code}" if country_code else city
            params = {"q": query}
            data = self._make_request("weather", params)
            if data:
                self._save_to_cache(cache_key, data)
            return data
        
        def get_forecast(self, city: str, country_code: str | None = None) -> Optional[Dict[str, Any]]:
            cache_key = f"forecast_{city}_{country_code}" if country_code else f"forecast_{city}"
            cached = self._get_cached_data(cache_key)
            if cached:
                cached["_from_cache"] = True
                return cached
            
            query = f"{city}, {country_code}" if country_code else city
            params = {"q": query}
            data = self._make_request("forecast", params)
            if data:
                self._save_to_cache(cache_key, data)
            return data