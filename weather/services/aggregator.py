import math

from .openweather import get_weather as openweather
from .weatherapi import get_weather as weatherapi


def get_aggregated_weather(city=None, lat=None, lon=None):
    results = []

    for service in [openweather, weatherapi]:
        try:
            data = service(city=city, lat=lat, lon=lon)
            results.append(data)
        except Exception:
            continue

    if not results:
        return {
            "city": city,
            "temperature": None,
            "description": "No data",
            "sources": []
        }

    avg_temp = sum(r["temperature"] for r in results) / len(results)
    avg_feels_like = sum(r["feels_like"] for r in results) / len(results)
    avg_humidity = sum(r["humidity"] for r in results) / len(results)
    avg_pressure = sum(r["pressure"] for r in results) / len(results)

    return {
        "city": results[0]["city"],
        "temperature": round(avg_temp, 1),
        "feels_like": round(avg_feels_like, 1),
        "humidity": round(avg_humidity, 1),
        "pressure": math.floor(avg_pressure),
        "description": [r["description"] for r in results],
        "sources": [r["source"] for r in results]
    }