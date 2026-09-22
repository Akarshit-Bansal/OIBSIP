from datetime import datetime
import webbrowser
from urllib.parse import quote


class CommandHandler:
    """Handles Ultron's voice commands."""

    def handle(self, intent, data=None):
        if data is None:
            data = {}

        if intent == "greeting":
            return "Hello Akarshit. How can I help you?"

        if intent == "time":
            current_time = datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}."

        if intent == "date":
            current_date = datetime.now().strftime("%A, %d %B %Y")
            return f"Today is {current_date}."

        if intent == "web_search":
            query = data.get("query", "")

            if not query:
                return "What would you like me to search for?"

            search_url = (
                "https://www.google.com/search?q="
                + quote(query)
            )

            webbrowser.open(search_url)

            return f"Searching the web for {query}."

        if intent == "exit":
            return "Goodbye Akarshit. Shutting down Ultron."

        return "I am still learning that command."