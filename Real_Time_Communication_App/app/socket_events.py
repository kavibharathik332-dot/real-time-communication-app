"""
app/socket_events.py
---------------------
This file handles everything that happens in REAL TIME:
  - a user coming online (connect)
  - a user going offline (disconnect)
  - sending a chat message
  - showing a "typing..." indicator

How rooms work:
  Every logged-in user automatically joins a private Socket.IO "room"
  named "user_<their id>", e.g. "user_101". To send User 101 a message,
  the server just emits an event to the room "user_101" -- Socket.IO
  makes sure only that user's browser receives it, even if they have
  the app open in more than one tab.
"""

from flask import session
from flask_socketio import join_room, leave_room, emit

from app import socketio
from app.database import get_user_by_id, save_message

# Keeps track of which usernames are currently online.
# Structure: { user_id: number_of_open_connections }
# We count connections (not just True/False) so that if a user has the
# app open in two browser tabs, closing one tab doesn't mark them offline.
online_users = {}


def _user_room(user_id):
    return f"user_{user_id}"


def _broadcast_status(user_id, is_online):
    """Tells every connected browser that a user's status changed."""
    user = get_user_by_id(user_id)
    if user is None:
        return
    emit(
        "status_update",
        {"user_id": user_id, "username": user["username"], "online": is_online},
        broadcast=True,
    )


@socketio.on("connect")
def handle_connect():
    user_id = session.get("user_id")
    if user_id is None:
        # Reject connections from anyone who is not logged in.
        return False

    join_room(_user_room(user_id))

    was_offline = online_users.get(user_id, 0) == 0
    online_users[user_id] = online_users.get(user_id, 0) + 1

    if was_offline:
        _broadcast_status(user_id, True)


@socketio.on("disconnect")
def handle_disconnect():
    user_id = session.get("user_id")
    if user_id is None:
        return

    if user_id in online_users:
        online_users[user_id] -= 1
        if online_users[user_id] <= 0:
            del online_users[user_id]
            leave_room(_user_room(user_id))
            _broadcast_status(user_id, False)


@socketio.on("get_online_users")
def handle_get_online_users():
    """Lets a freshly-loaded chat page ask 'who is online right now?'"""
    emit("online_users_list", {"online_user_ids": list(online_users.keys())})


@socketio.on("send_message")
def handle_send_message(data):
    """
    Expected data: { "receiver_id": 102, "message": "Hello Priya" }
    """
    sender_id = session.get("user_id")
    if sender_id is None:
        return

    receiver_id = data.get("receiver_id")
    message_text = (data.get("message") or "").strip()

    # ---- Validation ----
    if not receiver_id:
        emit("message_error", {"error": "No recipient selected."})
        return
    if not message_text:
        emit("message_error", {"error": "Message cannot be empty."})
        return
    if len(message_text) > 2000:
        emit("message_error", {"error": "Message is too long."})
        return

    receiver = get_user_by_id(receiver_id)
    if receiver is None:
        emit("message_error", {"error": "That user does not exist."})
        return

    # ---- Save to database ----
    saved = save_message(sender_id, receiver_id, message_text)

    # ---- Deliver in real time ----
    # Send to the receiver's private room...
    emit("new_message", saved, room=_user_room(receiver_id))
    # ...and echo back to the sender's own room, so it appears instantly
    # in the sender's chat window too (and syncs across their open tabs).
    emit("new_message", saved, room=_user_room(sender_id))


@socketio.on("typing")
def handle_typing(data):
    """
    Expected data: { "receiver_id": 102, "is_typing": true }
    Tells the receiver that the sender is (or isn't) currently typing.
    """
    sender_id = session.get("user_id")
    if sender_id is None:
        return

    receiver_id = data.get("receiver_id")
    is_typing = bool(data.get("is_typing"))
    if not receiver_id:
        return

    sender = get_user_by_id(sender_id)
    if sender is None:
        return

    emit(
        "typing_update",
        {"sender_id": sender_id, "username": sender["username"], "is_typing": is_typing},
        room=_user_room(receiver_id),
    )
