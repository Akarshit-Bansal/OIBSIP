import re


# ============================================================
# EMOJI SHORTCODES
# ============================================================

EMOJI_MAP = {
    ":smile:": "😄",
    ":laugh:": "😂",
    ":heart:": "❤️",
    ":love:": "😍",
    ":wink:": "😉",
    ":sad:": "😢",
    ":cry:": "😭",
    ":angry:": "😠",
    ":surprised:": "😮",
    ":cool:": "😎",
    ":thumbsup:": "👍",
    ":thumbsdown:": "👎",
    ":clap:": "👏",
    ":fire:": "🔥",
    ":rocket:": "🚀",
    ":party:": "🥳",
    ":ok:": "👌",
    ":wave:": "👋",
    ":pray:": "🙏",
    ":check:": "✅",
    ":warning:": "⚠️",
    ":star:": "⭐",
    ":sun:": "☀️",
    ":coffee:": "☕",
    ":computer:": "💻",
    ":python:": "🐍",
}


def convert_shortcodes(message):
    """
    Convert supported emoji shortcodes to Unicode emoji.

    Example:
        Hello :smile:
        ->
        Hello 😄
    """

    if not message:
        return message

    for shortcode, emoji in EMOJI_MAP.items():
        message = message.replace(
            shortcode,
            emoji
        )

    return message


def clean_message(message):
    """
    Remove unnecessary whitespace from a message.
    """

    if message is None:
        return ""

    return message.strip()


def validate_username(username):
    """
    Validate a chat username.
    """

    username = clean_message(username)

    if not username:
        return False, "Username cannot be empty."

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."

    if len(username) > 30:
        return False, "Username cannot exceed 30 characters."

    if not re.match(
        r"^[A-Za-z0-9_.-]+$",
        username
    ):
        return (
            False,
            "Username may contain letters, numbers, _, . and - only."
        )

    return True, ""


def validate_room_name(room_name):
    """
    Validate a chat room name.
    """

    room_name = clean_message(room_name)

    if not room_name:
        return False, "Room name cannot be empty."

    if len(room_name) > 50:
        return False, "Room name cannot exceed 50 characters."

    return True, ""


def format_timestamp(timestamp):
    """
    Convert an ISO timestamp into a readable time.

    Falls back to the original value if parsing fails.
    """

    if not timestamp:
        return ""

    try:
        from datetime import datetime

        value = datetime.fromisoformat(
            timestamp
        )

        return value.strftime(
            "%H:%M:%S"
        )

    except (ValueError, TypeError):
        return str(timestamp)


def format_chat_message(
    username,
    message,
    timestamp
):
    """
    Format a chat message for display.
    """

    time_text = format_timestamp(
        timestamp
    )

    return (
        f"[{time_text}] "
        f"{username}: "
        f"{message}"
    )