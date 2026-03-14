# tests/test_parser.py
from weather_app.weather_parser import (
    parse_current_weather,
    parse_forecast,
    c_to_f,
    format_dt,
)

def test_c_to_f_conversion():
    assert c_to_f(0) == 32
    assert c_to_f(100) == 212

def test_format_dt_returns_string():
    ts = 1700000000  # some timestamp
    s = format_dt(ts, 0)
    assert isinstance(s, str)
    assert "-" in s  # simple sanity check

def test_parse_current_weather_structure():
    raw = {
        "name": "TestCity",
        "sys": {"country": "TC", "sunrise": 1700000000, "sunset": 1700040000},
        "main": {"temp": 20, "feels_like": 18, "humidity": 80, "pressure": 1000},
        "wind": {"speed": 3.5},
        "weather": [{"description": "light rain"}],
        "visibility": 6000,
        "dt": 1700000000,
        "timezone": 0,
    }
    parsed = parse_current_weather(raw, unit="C")
    assert parsed["city"] == "TestCity"
    assert parsed["country"] == "TC"
    assert parsed["temp"] == 20
    assert parsed["feels_like"] == 18
    assert parsed["humidity"] == 80
    assert parsed["pressure"] == 1000
    assert parsed["visibility_km"] == 6
    assert "last_updated" in parsed
    assert parsed["description"] == "Light Rain"

def test_parse_forecast_aggregates_by_date():
    raw = {
        "city": {"timezone": 0},
        "list": [
            {
                "dt_txt": "2024-01-01 00:00:00",
                "main": {"temp": 10, "humidity": 80},
                "weather": [{"description": "clear sky"}],
            },
            {
                "dt_txt": "2024-01-01 03:00:00",
                "main": {"temp": 12, "humidity": 70},
                "weather": [{"description": "clear sky"}],
            },
        ],
    }
    daily = parse_forecast(raw, unit="C")
    assert len(daily) == 1
    day = daily[0]
    assert day["date"] == "2024-01-01"
    assert day["min"] == 10
    assert day["max"] == 12
    assert day["avg_humidity"] == 75
    assert day["description"] == "Clear Sky"
