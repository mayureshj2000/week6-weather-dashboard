import os
from pathlib import Path
import time
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = "760e12eb9ee8e82f4f3698236b27ebb1"
BASE_URL = "https://api.openweathermap.org/data/2.5"

DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"
FAVORITES_FILE = BASE_DIR / "favourites.json"

# Ensure directories exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True,exist_ok=True)
if not FAVORITES_FILE.exists():
    FAVORITES_FILE.write_text("[]")