import os

import requests
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

weather_api_url = "https://api.openweathermap.org/data/2.5/weather"


def get_current_weather(city: str, units: str = "imperial") -> dict:
    if units not in ["imperial", "metric", "standard"]:
        raise ValueError("units must be either 'imperial' or 'metric'")
    url = f"{weather_api_url}?q={city}&units={units}&appid={WEATHER_API_KEY}"
    response = requests.get(url)
    return response.json()
