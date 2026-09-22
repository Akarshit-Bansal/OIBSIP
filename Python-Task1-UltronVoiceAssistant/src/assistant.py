from src.speech import SpeechEngine
from src.intents import detect_intent
from src.commands import CommandHandler


class UltronAssistant:
    """Main controller for the Ultron voice assistant."""

    def __init__(self, microphone_index=1):
        self.speech = SpeechEngine(
            microphone_index=microphone_index
        )

        self.commands = CommandHandler()

        self.running = True

    def run(self):
        """Start the continuous voice assistant."""

        self.speech.speak(
            "Hello Akarshit. Ultron is online. "
            "How can I help you?"
        )

        while self.running:

            text = self.speech.listen()

            if not text:
                continue

            intent, data = detect_intent(text)

            response = self.commands.handle(
                intent,
                data
            )

            self.speech.speak(response)

            if intent == "exit":
                self.running = False