import hashlib
import secrets
import sqlite3
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATA_DIR / "chat.db"


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (room_id)
                REFERENCES rooms(id)
                ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            """
            INSERT OR IGNORE INTO rooms
                (name, created_at)
            VALUES
                (?, ?)
            """,
            (
                "General",
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        connection.commit()

    finally:
        connection.close()


def hash_password(password):

    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    ).hex()

    return password_hash, salt


def verify_password(
    password,
    stored_hash,
    stored_salt
):

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        stored_salt.encode("utf-8"),
        100_000
    ).hex()

    return secrets.compare_digest(
        password_hash,
        stored_hash
    )


def register_user(
    username,
    password
):

    username = username.strip()

    if not username:
        return False, "Username cannot be empty."

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."

    if len(username) > 30:
        return False, "Username cannot exceed 30 characters."

    if not password:
        return False, "Password cannot be empty."

    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    password_hash, salt = hash_password(password)

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO users
                (
                    username,
                    password_hash,
                    password_salt,
                    created_at
                )
            VALUES
                (?, ?, ?, ?)
            """,
            (
                username,
                password_hash,
                salt,
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        connection.commit()

        return True, "Registration successful."

    except sqlite3.IntegrityError:

        return False, "Username already exists."

    except sqlite3.Error as error:

        return False, f"Database error: {error}"

    finally:

        connection.close()


def authenticate_user(
    username,
    password
):

    username = username.strip()

    connection = get_connection()

    try:

        row = connection.execute(
            """
            SELECT
                username,
                password_hash,
                password_salt
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        if row is None:
            return False

        return verify_password(
            password,
            row["password_hash"],
            row["password_salt"]
        )

    except sqlite3.Error:

        return False

    finally:

        connection.close()


def create_room(room_name):

    room_name = room_name.strip()

    if not room_name:
        return False, "Room name cannot be empty."

    if len(room_name) > 50:
        return False, "Room name cannot exceed 50 characters."

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO rooms
                (name, created_at)
            VALUES
                (?, ?)
            """,
            (
                room_name,
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        connection.commit()

        return True, "Room created successfully."

    except sqlite3.IntegrityError:

        return False, "Room already exists."

    except sqlite3.Error as error:

        return False, f"Database error: {error}"

    finally:

        connection.close()


def get_rooms():

    connection = get_connection()

    try:

        rows = connection.execute(
            """
            SELECT
                id,
                name,
                created_at
            FROM rooms
            ORDER BY name
            """
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:

        connection.close()


def get_room_by_name(room_name):

    connection = get_connection()

    try:

        row = connection.execute(
            """
            SELECT
                id,
                name,
                created_at
            FROM rooms
            WHERE name = ?
            """,
            (room_name,)
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:

        connection.close()


def save_message(
    room_name,
    username,
    message
):

    room = get_room_by_name(room_name)

    if room is None:
        return False

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO messages
                (
                    room_id,
                    username,
                    message,
                    created_at
                )
            VALUES
                (?, ?, ?, ?)
            """,
            (
                room["id"],
                username,
                message,
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            ),
        )

        connection.commit()

        return True

    except sqlite3.Error:

        return False

    finally:

        connection.close()


def get_message_history(
    room_name,
    limit=100
):

    room = get_room_by_name(room_name)

    if room is None:
        return []

    connection = get_connection()

    try:

        rows = connection.execute(
            """
            SELECT
                username,
                message,
                created_at
            FROM messages
            WHERE room_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                room["id"],
                limit
            )
        ).fetchall()

        messages = [
            dict(row)
            for row in rows
        ]

        messages.reverse()

        return messages

    finally:

        connection.close()


initialize_database()
