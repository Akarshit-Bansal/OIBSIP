# OIBSIP Task 3 - Random Password Generator

## Overview

This project is an advanced Random Password Generator developed in Python as part of the Oasis Infobyte Python Programming Internship.

The application provides a graphical user interface for generating secure passwords based on user-defined requirements.

## Features

- Secure password generation using Python's `secrets` module
- Tkinter graphical user interface
- Password length selection from 8 to 128 characters
- Uppercase character selection
- Lowercase character selection
- Number selection
- Symbol selection
- Minimum two character-type validation
- Guaranteed inclusion of at least one character from every selected type
- Optional exclusion of ambiguous characters
- Weak / Medium / Strong password strength indicator
- Copy password to clipboard using `pyperclip`
- Automatic clipboard copy after password generation
- Last 5 generated passwords displayed during the current session
- Password history is not stored permanently
- Input validation and error handling

## Technology Stack

- Python 3
- Tkinter
- secrets
- string
- pyperclip

## Project Structure

```text
Python-Task3-RandomPasswordGenerator/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── password_generator.py
│
├── screenshots/
│
├── README.md
├── requirements.txt
└── .gitignore