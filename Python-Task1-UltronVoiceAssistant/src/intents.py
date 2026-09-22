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

    # Greeting
    greeting_patterns = [
        r"\bhello\b",
        r"\bhi\b",
        r"\bhey\b",
        r"\bgood morning\b",
        r"\bgood afternoon\b",
        r"\bgood evening\b",
    ]

    if any(re.search(pattern, text) for pattern in greeting_patterns):
        return "greeting", {}

    # Current time
    time_patterns = [
        r"\bwhat time is it\b",
        r"\bcurrent time\b",
        r"\btell me the time\b",
        r"\btime right now\b",
    ]

    if any(re.search(pattern, text) for pattern in time_patterns):
        return "time", {}

    # Current date
    date_patterns = [
        r"\bwhat is today's date\b",
        r"\bwhat's today's date\b",
        r"\btoday's date\b",
        r"\bcurrent date\b",
        r"\bwhat date is it\b",
    ]

    if any(re.search(pattern, text) for pattern in date_patterns):
        return "date", {}

    # Web search
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

    # Exit
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

    return "unknown", {}