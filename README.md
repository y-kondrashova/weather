# Weather API (Django + DRF)

A weather aggregation backend built with Django and Django REST Framework.
The application fetches data from multiple external weather APIs, normalizes it, and returns a unified response.

---

## Features

* User registration & authentication (Token-based)
* Weather search by:

  * City name
  * Latitude & Longitude
  
* Integration with multiple external weather APIs
* Aggregated and normalized weather data
* Optional database storage of weather results
* Protected endpoints (auth required)

---

## Tech Stack

* Python 3.14
* Django
* Django REST Framework
* Token Authentication (`rest_framework.authtoken`)
* External APIs (OpenWeather, WeatherAPI)

---

## Installation

### 1. Clone repo

```bash
git clone https://github.com/y-kondrashova/weather.git
cd weather
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set environment variables

Create `.env` file:

```env

OPENWEATHER_API_KEY=your_key
WEATHERAPI_KEY=your_key
```

---

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Run server

```bash
python manage.py runserver
```

---

## Running Tests

```bash
python manage.py test
```

Tests cover:

* user registration
* login
* authentication
* protected endpoints

---

## How it works

1. The client sends a request with either:
   * city
   * or latitude and longitude
2. The request is validated via serializers.
3. The system calls multiple weather providers (OpenWeather, WeatherAPI) through dedicated service modules.
4. Each provider response is normalized into a common internal format.
5. The aggregator:
   * combines results
   * filters failed responses
   * calculates aggregated values (average temperature, average pressure, average humidity, average feels like)
   * The final response is returned to the user and stored in the database.
   