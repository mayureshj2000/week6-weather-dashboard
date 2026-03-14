# tests/test_display.py
from io import StringIO
import sys

from weather_app.weather_display import show_current, show_forecast

def capture_output(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        func(*args, **kwargs)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

def test_show_current_prints_dashboard():
    current = {
        "city": "TestCity",
        "country": "TC",
        "last_updated": "2024-01-01 12:00",
        "temp": 20,
        "feels_like": 18,
        "unit": "°C",
        "description": "Clear Sky",
        "icon": "",
        "humidity": 80,
        "wind_speed": 3.5,
        "pressure": 1000,
        "visibility_km": 6,
        "sunrise": "2024-01-01 06:00",
        "sunset": "2024-01-01 18:00",
        "_from_cache": False,
    }
    out = capture_output(show_current, current)
    assert "WEATHER DASHBOARD" in out
    assert "TestCity" in out
    assert "20" in out

def test_show_forecast_prints_days():
    daily = [
        {
            "date": "2024-01-01",
            "min": 10,
            "max": 15,
            "avg_humidity": 70,
            "description": "Clear Sky",
        },
        {
            "date": "2024-01-02",
            "min": 11,
            "max": 16,
            "avg_humidity": 65,
            "description": "Clouds",
        },
    ]
    out = capture_output(show_forecast, daily)
    assert "5-Day Forecast" in out
    assert "2024-01-01" in out
    assert "2024-01-02" in out
