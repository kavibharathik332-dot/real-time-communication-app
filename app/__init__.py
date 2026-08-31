"""
app/__init__.py
----------------
This file creates and configures the Flask application.
It is the "starting point" that wires together the database,
the routes (pages), and the real-time Socket.IO server.
"""

import os
from flask import Flask
from flask_socketio import SocketIO

# This object lets us send/receive real-time messages.
# It is created here (empty) and "attached" to the app in create_app().
socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    """Creates and configures the Flask application."""

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # SECRET_KEY is used by Flask to keep user sessions (logins) secure.
    # It should NEVER be hard-coded in real projects. We read it from an
    # environment variable, and fall back to a random value if missing
    # (this fallback is fine for quick local testing only).
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-this"
    )

    # Path to the SQLite database file. It lives inside the "instance"
    # folder, which Flask treats as a safe place for local data files.
    os.makedirs(app.instance_path, exist_ok=True)
    app.config["DATABASE"] = os.path.join(app.instance_path, "chat.db")

    # Set up the database (creates tables if they do not exist yet).
    from app.database import init_db
    init_db(app)

    # Register the web pages (login, register, chat, etc.)
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Attach Socket.IO (real-time messaging) to this Flask app.
    socketio.init_app(app)

    # Register the real-time event handlers (connect, send_message, etc.)
    from app import socket_events  # noqa: F401  (import registers handlers)

    return app
