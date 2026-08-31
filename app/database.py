"""
app/database.py
----------------
This file manages the SQLite database.
It knows how to:
  - open a connection to the database file
  - create the USERS and MESSAGES tables (only if they don't already exist)
  - provide small helper functions used by routes.py and socket_events.py
"""

import sqlite3
from datetime import datetime, timezone
from flask import current_app, g


def get_db():
    """
    Returns a database connection for the current request.
    Flask's 'g' object stores one connection per request, so we don't
    open a new connection every single time we need one.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # This makes rows behave like dictionaries (row["username"])
        # instead of plain tuples (row[1]) -- much easier to read.
        g.db.row_factory = sqlite3.Row
        # Enforce foreign key constraints (sender_id/receiver_id must exist)
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """Closes the database connection at the end of each request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """
    Creates the USERS and MESSAGES tables if they do not exist yet.
    This runs once when the application starts.
    """
    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"])
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (sender_id) REFERENCES users (id),
                FOREIGN KEY (receiver_id) REFERENCES users (id)
            )
            """
        )
        db.commit()
        db.close()

    # Make sure the connection closes automatically after each request.
    app.teardown_appcontext(close_db)


def now_iso():
    """Returns the current UTC time as a text string, for timestamps."""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------
# Small reusable helper functions (used by routes.py / socket_events.py)
# ---------------------------------------------------------------------

def get_user_by_username(username):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()


def get_user_by_id(user_id):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()


def create_user(username, password_hash):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
        (username, password_hash, now_iso()),
    )
    db.commit()
    return cursor.lastrowid


def get_all_users_except(user_id):
    db = get_db()
    return db.execute(
        "SELECT id, username FROM users WHERE id != ? ORDER BY username COLLATE NOCASE",
        (user_id,),
    ).fetchall()


def save_message(sender_id, receiver_id, message):
    db = get_db()
    created_at = now_iso()
    cursor = db.execute(
        """
        INSERT INTO messages (sender_id, receiver_id, message, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (sender_id, receiver_id, message, created_at),
    )
    db.commit()
    return {
        "id": cursor.lastrowid,
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "message": message,
        "created_at": created_at,
    }


def get_conversation(user_a_id, user_b_id):
    """Returns all messages exchanged between two users, oldest first."""
    db = get_db()
    rows = db.execute(
        """
        SELECT id, sender_id, receiver_id, message, created_at
        FROM messages
        WHERE (sender_id = ? AND receiver_id = ?)
           OR (sender_id = ? AND receiver_id = ?)
        ORDER BY id ASC
        """,
        (user_a_id, user_b_id, user_b_id, user_a_id),
    ).fetchall()
    return [dict(row) for row in rows]
