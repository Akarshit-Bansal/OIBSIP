import threading
import time


class ReminderManager:
    """Manages timed reminders for Ultron."""

    def __init__(self, speak_callback):
        self.speak = speak_callback
        self.active_reminders = []

    def add_reminder(self, message, delay_seconds):
        """Schedule a reminder after a specified number of seconds."""

        timer = threading.Timer(
            delay_seconds,
            self._trigger_reminder,
            args=(message,)
        )

        timer.daemon = True
        timer.start()

        self.active_reminders.append(timer)

        return (
            f"Reminder set for {delay_seconds} seconds from now."
        )

    def _trigger_reminder(self, message):
        """Trigger the reminder."""

        self.speak(
            f"Reminder: {message}"
        )

        print(
            f"Reminder triggered: {message}"
        )

    def cancel_all(self):
        """Cancel all active reminders."""

        for timer in self.active_reminders:
            timer.cancel()

        self.active_reminders.clear()