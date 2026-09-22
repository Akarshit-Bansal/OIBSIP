from src.speech import SpeechEngine


def main():
    assistant = SpeechEngine(microphone_index=1)

    assistant.speak(
        "Hello Akarshit. Ultron is ready."
    )

    text = assistant.listen()

    if text:
        assistant.speak(
            f"I heard you say {text}"
        )


if __name__ == "__main__":
    main()