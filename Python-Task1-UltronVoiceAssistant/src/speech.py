import speech_recognition as sr
import pyttsx3


class SpeechEngine:
    """Handles speech input and voice output for Ultron."""

    def __init__(self, microphone_index=1):
        self.microphone_index = microphone_index

        # Speech recognition
        self.recognizer = sr.Recognizer()

        # Text-to-speech
        self.engine = pyttsx3.init()

        # Configure voice speed
        self.engine.setProperty("rate", 175)

        # Configure microphone
        self.microphone = sr.Microphone(
            device_index=self.microphone_index
        )

    def speak(self, text):
        """Convert text to speech."""
        print(f"Ultron: {text}")

        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen to the microphone and convert speech to text."""

        with self.microphone as source:
            print("Listening...")

            # Adjust for background noise
            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=7
                )

            except sr.WaitTimeoutError:
                print("No speech detected.")
                return None

        print("Processing...")

        try:
            text = self.recognizer.recognize_google(audio)

            print(f"You: {text}")

            return text.lower()

        except sr.UnknownValueError:
            self.speak(
                "Sorry, I could not understand what you said."
            )
            return None

        except sr.RequestError as error:
            print(f"Speech recognition error: {error}")

            self.speak(
                "I am having trouble connecting to the speech recognition service."
            )

            return None