import os

import requests
from dotenv import load_dotenv


load_dotenv()


class WeatherService:
    """Fetches current weather information."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

    def get_weather(self, city):
        """Get current weather for a city."""

        if not self.api_key or self.api_key == "YOUR_API_KEY_HERE":
            return (
                "Weather service is not configured yet. "
                "Please add your OpenWeather API key."
            )

        if not city:
            return (
                "Please tell me the city you want "
                "the weather for."
            )

        try:
            response = requests.get(
                self.BASE_URL,
                params={
                    "q": city,
                    "appid": self.api_key,
                    "units": "metric",
                },
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            temperature = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]

            return (
                f"The weather in {city} is {description}. "
                f"The temperature is {temperature:.1f} degrees Celsius, "
                f"feels like {feels_like:.1f} degrees, "
                f"with {humidity}% humidity."
            )

        except requests.exceptions.HTTPError:
            return (
                "I could not find weather information "
                f"for {city}."
            )

        except requests.exceptions.RequestException:
            return (
                "I could not connect to the weather service "
                "right now."
            )

        except (KeyError, TypeError, ValueError):
            return (
                "The weather service returned an unexpected response."
            )