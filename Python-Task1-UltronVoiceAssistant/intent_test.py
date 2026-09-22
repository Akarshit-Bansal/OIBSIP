from src.intents import detect_intent
from src.commands import CommandHandler


def main():
    handler = CommandHandler()

    test_commands = [
        "hello Ultron",
        "what time is it",
        "what is today's date",
        "goodbye",
        "search for Python FastAPI tutorials",
        "tell me something interesting",
    ]

    for command in test_commands:
        print(f"\nUser: {command}")

        intent, data = detect_intent(command)

        print(f"Intent: {intent}")

        response = handler.handle(intent, data)

        print(f"Ultron: {response}")


if __name__ == "__main__":
    main()