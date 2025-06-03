#!/usr/bin/env python3
"""
Basic Flask app module.

This module sets up a simple Flask web application with routes for
user registration, session management, profile retrieval, and
password reset/update functionalities.
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index() -> dict:
    """
    GET /

    Returns a JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> tuple:
    """
    POST /users

    Registers a new user based on 'email' and 'password' form data.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def sessions() -> tuple:
    """
    POST /sessions

    Handles user login. Expects 'email' and 'password' form data.
    If login is incorrect, aborts with 401 Unauthorized.
    Otherwise, creates a session, sets a 'session_id' cookie,
    and returns a JSON payload.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response_data = {"email": email, "message": "logged in"}
    response = make_response(jsonify(response_data))
    response.set_cookie("session_id", session_id)

    return response, 200


@app.route("/sessions", methods=["DELETE"])
def destroy_session_route() -> tuple:
    """
    DELETE /sessions

    Handles user logout. Expects 'session_id' in cookies.
    If user exists, destroys session and redirects to GET /.
    Otherwise, responds with 403 Forbidden.
    """
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        return redirect("/")


@app.route("/profile", methods=["GET"])
def profile() -> tuple:
    """
    GET /profile

    Retrieves user profile based on session ID cookie.
    If user exists, returns JSON payload with email (200 OK).
    If session ID is invalid or user not found, aborts with 403 Forbidden.
    """
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
    else:
        return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token_route() -> tuple:
    """
    POST /reset_password

    Handles password reset token generation. Expects 'email' form data.
    If email is not registered, responds with 403 Forbidden.
    Otherwise, generates a token and returns a JSON payload.
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password_route() -> tuple:
    """
    PUT /reset_password

    Handles updating user password using a reset token.
    Expects 'email', 'reset_token', and 'new_password' form data.
    If the token is invalid, responds with 403 Forbidden.
    Otherwise, updates the password and responds with 200 OK.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        # Update the password using the Auth class method
        AUTH.update_password(reset_token, new_password)
        # If successful, return the success message
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        # If ValueError is raised (meaning invalid token), abort with 403
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
