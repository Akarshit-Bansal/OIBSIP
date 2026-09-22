import re


def detect_intent(text):
    """
    Detect the user's intent from natural language.

    Returns:
        tuple: (intent_name, extracted_data)
    """

    if not text:
        return "unknown", {}

    text = text.lower().strip()

    # ---------------------------------------------------------
    # Exit
    # ---------------------------------------------------------
    exit_patterns = [
        r"\bexit\b",
        r"\bquit\b",
        r"\bgoodbye\b",
        r"\bgood bye\b",
        r"\bstop listening\b",
        r"\bstop\b",
    ]

    if any(re.search(pattern, text) for pattern in exit_patterns):
        return "exit", {}

        # ---------------------------------------------------------
    # Reminder
    # ---------------------------------------------------------
    reminder_patterns = [
        r"\bremind me in (\d+)\s*(seconds?|minutes?|hours?)\s*(?:to\s+)?(.+)",
        r"\bset a reminder in (\d+)\s*(seconds?|minutes?|hours?)\s*(?:to\s+)?(.+)",
    ]

    for pattern in reminder_patterns:
        match = re.search(pattern, text)

        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            message = match.group(3).strip()

            if unit.startswith("second"):
                delay_seconds = amount

            elif unit.startswith("minute"):
                delay_seconds = amount * 60

            elif unit.startswith("hour"):
                delay_seconds = amount * 60 * 60

            else:
                delay_seconds = amount

            return "reminder", {
                "message": message,
                "delay_seconds": delay_seconds,
            }
    # ---------------------------------------------------------
    # Web search
    # ---------------------------------------------------------
    search_patterns = [
        r"\bsearch the web for (.+)",
        r"\bsearch the web (.+)",
        r"\bsearch for (.+)",
        r"\bsearch (.+)",
        r"\bgoogle (.+)",
        r"\blook up (.+)",
        r"\bfind information about (.+)",
    ]

    for pattern in search_patterns:
        match = re.search(pattern, text)

        if match:
            query = match.group(1).strip()

            return "web_search", {
                "query": query
            }

    # ---------------------------------------------------------
    # Weather
    # ---------------------------------------------------------
    weather_patterns = [
        r"\bwhat is the weather\b(?: today)?(?: in (.+))?",
        r"\bwhat's the weather\b(?: today)?(?: in (.+))?",
        r"\bweather today\b(?: in (.+))?",
        r"\bweather\b(?: in (.+))?",
        r"\btemperature\b(?: today)?(?: in (.+))?",
        r"\bwhat is the temperature\b(?: today)?(?: in (.+))?",
    ]

    for pattern in weather_patterns:
        match = re.search(pattern, text)

        if match:
            city = None

            if match.lastindex and match.group(match.lastindex):
                city = match.group(match.lastindex).strip()

            return "weather", {
                "city": city
            }

    # ---------------------------------------------------------
    # Current time
    # ---------------------------------------------------------
    time_patterns = [
        r"\bwhat time is it\b",
        r"\bwhat is the time\b",
        r"\bwhat's the time\b",
        r"\bcurrent time\b",
        r"\btell me the time\b",
        r"\btime right now\b",
        r"\bwhat time\b",
    ]

    if any(re.search(pattern, text) for pattern in time_patterns):
        return "time", {}

    # ---------------------------------------------------------
    # Current date
    # ---------------------------------------------------------
    date_patterns = [
        r"\bwhat is today's date\b",
        r"\bwhat's today's date\b",
        r"\bwhat is the date today\b",
        r"\bwhat's the date today\b",
        r"\btoday's date\b",
        r"\bdate today\b",
        r"\bcurrent date\b",
        r"\bwhat date is it\b",
        r"\btell me the date\b",
        r"\btell me today's date\b",
    ]

    if any(re.search(pattern, text) for pattern in date_patterns):
        return "date", {}

    # ---------------------------------------------------------
    # Greeting
    # ---------------------------------------------------------
    greeting_patterns = [
        r"^\s*hello\s*(?:ultron)?\s*$",
        r"^\s*hi\s*(?:ultron)?\s*$",
        r"^\s*hey\s*(?:ultron)?\s*$",
        r"^\s*good morning\s*(?:ultron)?\s*$",
        r"^\s*good afternoon\s*(?:ultron)?\s*$",
        r"^\s*good evening\s*(?:ultron)?\s*$",
    ]

    if any(re.search(pattern, text) for pattern in greeting_patterns):
        return "greeting", {}

    return "unknown", {}