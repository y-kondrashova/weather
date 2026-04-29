import math

from .openweather import get_weather as openweather
from .weatherapi import get_weather as weatherapi
from weather.models import Location, WeatherSource, CurrentWeather
from django.utils import timezone


def get_or_create_location(city, lat=None, lon=None):
    location, _ = Location.objects.get_or_create(
        city=city,
        defaults={
            "lat": lat or 0,
            "lon": lon or 0,
        }
    )
    return location

def get_or_create_source(name):
    source, _ = WeatherSource.objects.get_or_create(name=name)
    return source


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
            "feels_like": None,
            "humidity": None,
            "pressure": None,
            "description": ["No data"],
            "sources": []
        }

    location = get_or_create_location(
        city=results[0]["city"],
        lat=lat,
        lon=lon
    )

    for result in results:
        source = get_or_create_source(result["source"])

        CurrentWeather.objects.update_or_create(
            location=location,
            source=source,
            observed_at=timezone.now(),
            temperature=result["temperature"],
            feels_like=result["feels_like"],
            humidity=result["humidity"],
            pressure=result["pressure"],
            description=result["description"],
        )

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
