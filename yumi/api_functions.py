from typing import Any, Dict

import requests

from yumi.config import Config

configs = Config()

WEATHER_API_KEY = configs.WEATHER_API_KEY

weather_api_url = "https://api.openweathermap.org/data/2.5/weather"


def get_current_weather(weather_api: Dict[str, Any]) -> Dict[str, Any]:
    api_data = weather_api.get("weather_api")
    url = f"{weather_api_url}?q={api_data.city}&units={api_data.units}&appid={WEATHER_API_KEY}"  # noqa
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
