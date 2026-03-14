import os
import json
from pathlib import Path
import time
import pytest

from weather_app.config import CACHE_DIR, API_KEY
from weather_app.weather_api import WeatherAPI

@pytest.mark.skipif(not API_KEY, reason="WEATHER_API_KEY not set")
def test_get_current_weather_returns_dict():
    api = WeatherAPI()
    data = api.get_current_weather("London")
    assert data is None or isinstance(data, dict)

@pytest.mark.skipif(not API_KEY, reason="WEATHER_API_KEY not set")
def test_get_forecast_returns_dict():
    api = WeatherAPI()
    data = api.get_forecast("London")
    assert data is None or isinstance(data, dict)

def test_cache_read_write_roundtrip(tmp_path, monkeypatch):
    # Point cache dir to temp folder
    monkeypatch.setattr("weather_app.weather_api.CACHE_DIR", tmp_path)
    api = WeatherAPI(api_key="dummy", base_url="http://example.com")

    # Fake data
    key = "test_city"
    payload = {"foo": "bar"}

    # Save to cache
    api._save_to_cache(key, payload)
    cached = api._get_cached_data(key)
    assert cached == payload

    # Expire cache and ensure None is returned
    cache_file = tmp_path / f"{key}.json"
    old_time = time.time() - (api.cache_duration + 10)
    os.utime(cache_file, (old_time, old_time))
    expired = api._get_cached_data(key)
    assert expired is None