from src.intents import detect_intent
from src.commands import CommandHandler


def main():
    handler = CommandHandler()

    test_commands = [
        "hello Ultron what time is it",
	"tell me the date today",
	"tell me what is the weather today",
	"what is the weather in Delhi",
	"remind me in 10 seconds to drink water",
]

    for command in test_commands:
        print(f"\nUser: {command}")

        intent, data = detect_intent(command)

        print(f"Intent: {intent}")

        response = handler.handle(intent, data)

        print(f"Ultron: {response}")


if __name__ == "__main__":
    main()