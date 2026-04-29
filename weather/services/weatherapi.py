import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")


def get_weather(city=None, lat=None, lon=None):
    url = "http://api.weatherapi.com/v1/current.json"

    params = {
        "key": API_KEY,
    }

    if city:
        params["q"] = city
    else:
        params["q"] = f"{lat},{lon}"

    response = requests.get(url, params=params)
    data = response.json()

    return {
        "source": "weatherapi",
        "city": data["location"]["name"],
        "temperature": data["current"]["temp_c"],
        "feels_like": data["current"]["feelslike_c"],
        "humidity": data["current"]["humidity"],
        "pressure": data["current"]["pressure_mb"],
        "wind_speed": data["current"]["wind_kph"],
        "description": data["current"]["condition"]["text"],
    }