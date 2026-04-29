import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("OPENWEATHER_API_KEY")

def get_weather(city=None, lat=None, lon=None):
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {"appid": API_KEY, "units": "metric"}

    if city:
        params["q"] = city
    else:
        params["lat"] = lat
        params["lon"] = lon

    response = requests.get(url, params=params)
    data = response.json()

    return {
        "source": "openweather",
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
    }