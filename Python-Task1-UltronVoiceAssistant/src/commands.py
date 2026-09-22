from datetime import datetime
import webbrowser
from urllib.parse import quote

from src.reminders import ReminderManager
from src.weather import WeatherService


class CommandHandler:
    """Handles Ultron's voice commands."""

    def __init__(self, speak_callback=None):
        self.speak_callback = speak_callback

        if speak_callback:
            self.reminders = ReminderManager(
                speak_callback
            )
        else:
            self.reminders = None

        self.weather = WeatherService()

    def handle(self, intent, data=None):
        """Handle a detected intent and return a response."""

        if data is None:
            data = {}

        # ---------------------------------------------------------
        # Greeting
        # ---------------------------------------------------------
        if intent == "greeting":
            return "Hello Akarshit. How can I help you?"

        # ---------------------------------------------------------
        # Current time
        # ---------------------------------------------------------
        if intent == "time":
            current_time = datetime.now().strftime("%I:%M %p")

            return (
                f"The current time is {current_time}."
            )

        # ---------------------------------------------------------
        # Current date
        # ---------------------------------------------------------
        if intent == "date":
            current_date = datetime.now().strftime(
                "%A, %d %B %Y"
            )

            return (
                f"Today is {current_date}."
            )

        # ---------------------------------------------------------
        # Reminder
        # ---------------------------------------------------------
        if intent == "reminder":
            message = data.get("message", "")
            delay_seconds = data.get(
                "delay_seconds",
                0
            )

            if not message or delay_seconds <= 0:
                return (
                    "I could not understand the reminder."
                )

            if self.reminders:
                self.reminders.add_reminder(
                    message,
                    delay_seconds
                )

            return (
                f"Reminder set for "
                f"{delay_seconds} seconds from now."
            )

        # ---------------------------------------------------------
        # Weather
        # ---------------------------------------------------------
        if intent == "weather":
            city = data.get("city")

            return self.weather.get_weather(city)

        # ---------------------------------------------------------
        # Web search
        # ---------------------------------------------------------
        if intent == "web_search":
            query = data.get("query", "")

            if not query:
                return (
                    "What would you like me to search for?"
                )

            search_url = (
                "https://www.google.com/search?q="
                + quote(query)
            )

            webbrowser.open(search_url)

            return (
                f"Searching the web for {query}."
            )

        # ---------------------------------------------------------
        # Exit
        # ---------------------------------------------------------
        if intent == "exit":
            return (
                "Goodbye Akarshit. "
                "Shutting down Ultron."
            )

        # ---------------------------------------------------------
        # Unknown command
        # ---------------------------------------------------------
        return (
            "I am still learning that command."
        )