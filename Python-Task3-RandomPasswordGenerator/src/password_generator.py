import secrets
import string


# Characters that can easily be confused with each other.
AMBIGUOUS_CHARACTERS = "0Ol1I"


CHARACTER_SETS = {
    "uppercase": string.ascii_uppercase,
    "lowercase": string.ascii_lowercase,
    "numbers": string.digits,
    "symbols": "!@#$%^&*()-_=+[]{};:,.?/<>",
}


def get_character_sets(
    use_uppercase=True,
    use_lowercase=True,
    use_numbers=True,
    use_symbols=True,
    exclude_ambiguous=True,
):
    """Return the selected character sets."""

    selected = []

    options = {
        "uppercase": use_uppercase,
        "lowercase": use_lowercase,
        "numbers": use_numbers,
        "symbols": use_symbols,
    }

    for name, enabled in options.items():
        if enabled:
            characters = CHARACTER_SETS[name]

            if exclude_ambiguous:
                characters = "".join(
                    char
                    for char in characters
                    if char not in AMBIGUOUS_CHARACTERS
                )

            selected.append(characters)

    return selected


def validate_options(
    length,
    use_uppercase,
    use_lowercase,
    use_numbers,
    use_symbols,
):
    """Validate password generation settings."""

    if length < 8:
        raise ValueError("Password length must be at least 8 characters.")

    selected_count = sum(
        [
            use_uppercase,
            use_lowercase,
            use_numbers,
            use_symbols,
        ]
    )

    if selected_count < 2:
        raise ValueError(
            "Please select at least two character types."
        )


def generate_password(
    length,
    use_uppercase=True,
    use_lowercase=True,
    use_numbers=True,
    use_symbols=True,
    exclude_ambiguous=True,
):
    """
    Generate a cryptographically secure password.

    At least one character from every selected character type
    is guaranteed to appear in the generated password.
    """

    validate_options(
        length,
        use_uppercase,
        use_lowercase,
        use_numbers,
        use_symbols,
    )

    selected_sets = get_character_sets(
        use_uppercase,
        use_lowercase,
        use_numbers,
        use_symbols,
        exclude_ambiguous,
    )

    if not selected_sets:
        raise ValueError("Select at least two character types.")

    # Guarantee at least one character from every selected type.
    password_characters = [
        secrets.choice(character_set)
        for character_set in selected_sets
    ]

    # Combine all selected character sets.
    combined_characters = "".join(selected_sets)

    remaining_length = length - len(password_characters)

    # Fill the remaining positions securely.
    password_characters.extend(
        secrets.choice(combined_characters)
        for _ in range(remaining_length)
    )

    # Securely shuffle the characters so guaranteed characters
    # aren't always placed at the beginning.
    for index in range(len(password_characters) - 1, 0, -1):
        swap_index = secrets.randbelow(index + 1)

        password_characters[index], password_characters[swap_index] = (
            password_characters[swap_index],
            password_characters[index],
        )

    return "".join(password_characters)


def calculate_strength(
    password,
    selected_type_count=None,
):
    """
    Classify password strength as Weak, Medium, or Strong.

    Strength considers both password length and character diversity.
    """

    length = len(password)

    if selected_type_count is None:
        selected_type_count = 0

        if any(char.isupper() for char in password):
            selected_type_count += 1

        if any(char.islower() for char in password):
            selected_type_count += 1

        if any(char.isdigit() for char in password):
            selected_type_count += 1

        if any(not char.isalnum() for char in password):
            selected_type_count += 1

    if length >= 16 and selected_type_count >= 4:
        return "Strong"

    if length >= 12 and selected_type_count >= 3:
        return "Strong"

    if length >= 10 and selected_type_count >= 2:
        return "Medium"

    return "Weak"