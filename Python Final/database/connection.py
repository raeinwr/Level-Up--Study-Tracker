"""Database layer: SQLite connection and schema."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "levelup.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    avatar TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS trackers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS topics(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracker_id INTEGER NOT NULL REFERENCES trackers(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    hours REAL NOT NULL,
    done INTEGER NOT NULL DEFAULT 0,
    studied_seconds INTEGER NOT NULL DEFAULT 0
);
"""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript(SCHEMA)

        # Upgrade databases created by the older version of the project.
        columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(topics)")
        }

        if "studied_seconds" not in columns:
            conn.execute(
                "ALTER TABLE topics ADD COLUMN studied_seconds INTEGER NOT NULL DEFAULT 0"
            )
