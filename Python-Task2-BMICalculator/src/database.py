import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "bmi_records.db"


def initialize_database():
    """Create the database and BMI records table if they don't exist."""

    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    recorded_at TEXT NOT NULL
                )
            """)

            connection.commit()

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Database initialization failed: {error}"
        )


def save_bmi_record(user_name, weight, height, bmi, category):
    """Save a BMI calculation to the database."""

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO bmi_records
                (user_name, weight, height, bmi, category, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_name,
                weight,
                height,
                bmi,
                category,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            connection.commit()

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to save BMI record: {error}"
        )


def get_user_history(user_name):
    """Return all BMI records for a specific user."""

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.row_factory = sqlite3.Row

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    user_name,
                    weight,
                    height,
                    bmi,
                    category,
                    recorded_at
                FROM bmi_records
                WHERE user_name = ?
                ORDER BY recorded_at ASC
            """, (user_name,))

            return [dict(row) for row in cursor.fetchall()]

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to retrieve BMI history: {error}"
        )


def get_all_users():
    """Return a list of all users stored in the database."""

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT DISTINCT user_name
                FROM bmi_records
                ORDER BY user_name
            """)

            return [row[0] for row in cursor.fetchall()]

    except sqlite3.Error as error:
        raise RuntimeError(
            f"Unable to retrieve users: {error}"
        )