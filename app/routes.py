"""
app/routes.py
-------------
This file defines all the web pages (routes) of the application:

    /            -> chat page (if logged in) or redirect to login
    /register    -> create a new account
    /login       -> log in to an existing account
    /logout      -> log out
    /api/users   -> JSON list of all other registered users
    /api/messages/<user_id> -> JSON chat history with one user

It also implements username/password authentication using Flask's
built-in "session" (a secure cookie) and Werkzeug's password hashing.
"""

from functools import wraps

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, session, jsonify, flash
)
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import (
    get_user_by_username, get_user_by_id, create_user,
    get_all_users_except, get_conversation
)

main_bp = Blueprint("main", __name__)


def login_required(view):
    """
    A decorator that protects a page so only logged-in users can see it.
    If nobody is logged in, the user is redirected to the login page.
    """
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)
    return wrapped_view


# ---------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------

@main_bp.route("/")
@login_required
def index():
    """The main chat page. Only visible after logging in."""
    return render_template(
        "chat.html",
        username=session.get("username"),
        user_id=session.get("user_id"),
    )


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        error = None
        if not username or not password:
            error = "Username and password are required."
        elif len(username) < 3:
            error = "Username must be at least 3 characters long."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif get_user_by_username(username) is not None:
            error = "That username is already taken. Please choose another."

        if error:
            flash(error, "error")
            return render_template("register.html", username=username)

        password_hash = generate_password_hash(password)
        user_id = create_user(username, password_hash)

        # Automatically log the user in after registering.
        session.clear()
        session["user_id"] = user_id
        session["username"] = username
        return redirect(url_for("main.index"))

    return render_template("register.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        error = None
        user = get_user_by_username(username)

        if user is None:
            error = "Invalid username or password."
        elif not check_password_hash(user["password_hash"], password):
            error = "Invalid username or password."

        if error:
            flash(error, "error")
            return render_template("login.html", username=username)

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("main.index"))

    return render_template("login.html")


@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


# ---------------------------------------------------------------------
# JSON API endpoints (used by static/script.js)
# ---------------------------------------------------------------------

@main_bp.route("/api/users")
@login_required
def api_users():
    """Returns every registered user except the one currently logged in."""
    users = get_all_users_except(session["user_id"])
    return jsonify([{"id": u["id"], "username": u["username"]} for u in users])


@main_bp.route("/api/messages/<int:other_user_id>")
@login_required
def api_messages(other_user_id):
    """Returns the full chat history between the current user and another."""
    other_user = get_user_by_id(other_user_id)
    if other_user is None:
        return jsonify({"error": "User not found."}), 404

    messages = get_conversation(session["user_id"], other_user_id)
    return jsonify(messages)
