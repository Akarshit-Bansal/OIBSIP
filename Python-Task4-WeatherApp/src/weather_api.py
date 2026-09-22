import os
from datetime import datetime

import requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://api.openweathermap.org/data/2.5"
REQUEST_TIMEOUT = 10


class WeatherAPIError(Exception):
    """Base exception for weather API errors."""


class InvalidAPIKeyError(WeatherAPIError):
    """Raised when the OpenWeatherMap API key is invalid."""


class CityNotFoundError(WeatherAPIError):
    """Raised when the requested city cannot be found."""


class NetworkError(WeatherAPIError):
    """Raised when the weather API cannot be reached."""


def get_api_key():
    """Read the OpenWeatherMap API key from the environment."""

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        raise InvalidAPIKeyError(
            "OpenWeatherMap API key is missing. "
            "Please configure OPENWEATHER_API_KEY in .env."
        )

    return api_key


def request_api(endpoint, params):
    """Make a request to the OpenWeatherMap API."""

    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

    except requests.exceptions.Timeout as error:
        raise NetworkError(
            "The weather service timed out. Please try again."
        ) from error

    except requests.exceptions.ConnectionError as error:
        raise NetworkError(
            "Unable to connect to the weather service. "
            "Please check your internet connection."
        ) from error

    except requests.exceptions.RequestException as error:
        raise NetworkError(
            "A network error occurred while contacting the weather service."
        ) from error

    if response.status_code in (401, 403):
        raise InvalidAPIKeyError(
            "The OpenWeatherMap API key is invalid or not authorized."
        )

    if response.status_code == 404:
        raise CityNotFoundError(
            "The requested city could not be found."
        )

    if response.status_code == 429:
        raise WeatherAPIError(
            "OpenWeatherMap API rate limit reached. Please try again later."
        )

    try:
        response.raise_for_status()
        return response.json()

    except ValueError as error:
        raise WeatherAPIError(
            "The weather service returned an invalid response."
        ) from error

    except requests.exceptions.HTTPError as error:
        raise WeatherAPIError(
            f"Weather API request failed: HTTP {response.status_code}."
        ) from error


def get_current_weather(city):
    """
    Fetch current weather for a city.

    Returns temperature, humidity, weather condition,
    wind speed, icon and location information.
    """

    if not city or not city.strip():
        raise ValueError("Please enter a city name.")

    api_key = get_api_key()

    params = {
        "q": city.strip(),
        "appid": api_key,
        "units": "metric",
    }

    data = request_api("weather", params)

    weather = data["weather"][0]
    main = data["main"]
    wind = data["wind"]

    return {
        "city": data.get("name", city.strip()),
        "country": data.get("sys", {}).get("country", ""),
        "temperature_c": main.get("temp"),
        "feels_like_c": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "condition": weather.get("main", ""),
        "description": weather.get("description", "").title(),
        "wind_speed": wind.get("speed", 0),
        "icon": weather.get("icon", ""),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def get_forecast(city):
    """
    Fetch the OpenWeatherMap 5-day / 3-hour forecast.

    The response contains forecast entries approximately
    every three hours.
    """

    if not city or not city.strip():
        raise ValueError("Please enter a city name.")

    api_key = get_api_key()

    params = {
        "q": city.strip(),
        "appid": api_key,
        "units": "metric",
    }

    return request_api("forecast", params)