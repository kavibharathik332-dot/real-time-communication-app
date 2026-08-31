"""
run.py
------
This is the file you run to start the application locally.

Usage:
    python run.py

It starts the Flask-SocketIO development server on port 5000
(or on the PORT environment variable, if one is set -- this is
needed for hosting platforms like Render).
"""

import os
from app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # debug=False is safer; turn it on locally if you want auto-reload.
    socketio.run(app, host="0.0.0.0", port=port, debug=False, allow_unsafe_werkzeug=True)
