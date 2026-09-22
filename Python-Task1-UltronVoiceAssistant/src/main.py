from src.assistant import UltronAssistant


def main():
    """Application entry point."""

    assistant = UltronAssistant(
        microphone_index=1
    )

    try:
        assistant.run()

    except KeyboardInterrupt:
        print("\nUltron stopped by user.")


if __name__ == "__main__":
    main()