import time

from src.reminders import ReminderManager


def speak(message):
    print(f"ULTRON: {message}")


def main():
    reminders = ReminderManager(speak)

    response = reminders.add_reminder(
        "Drink water",
        10
    )

    print(response)

    print("Waiting for reminder...")

    time.sleep(12)


if __name__ == "__main__":
    main()