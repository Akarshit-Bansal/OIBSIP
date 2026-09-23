# OIBSIP Task 5 - Real-Time Chat Application

A real-time desktop chat application developed in Python as part of the Oasis Infobyte Python Programming Internship.

The application uses a Tkinter graphical interface, TCP sockets for real-time communication, SQLite for user authentication, rooms and message history, and Python's standard library for the core implementation.

---

## Features

### Authentication
- User registration
- Username and password login
- Passwords are not stored as plaintext
- Salted PBKDF2-HMAC-SHA256 password hashing
- SQLite-based authentication

### Real-Time Chat
- TCP socket communication
- Real-time bidirectional messaging
- Multiple clients supported simultaneously
- Message timestamps
- Graceful client disconnection
- Localhost server

### Chat Rooms
- General room available by default
- Create new chat rooms
- Join existing rooms
- Multiple users can participate in the same room
- Room-specific message history

### Message History
- Messages are stored in SQLite
- Last 100 messages are loaded when joining a room
- Historical messages include username, message and timestamp

### Emoji Shortcodes

The application converts supported shortcodes into Unicode emoji.

Examples:

```text
:smile:      -> 😄
:laugh:      -> 😂
:heart:      -> ❤️
:thumbsup:   -> 👍
:fire:       -> 🔥
:rocket:     -> 🚀
:python:     -> 🐍