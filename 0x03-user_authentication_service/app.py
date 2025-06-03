#!/usr/bin/env python3
"""
Basic Flask app module.

This module sets up a simple Flask web application with routes for
user registration and session management.
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

    # Find the user associated with the session_id
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        # If no user found for the session_id, respond with 403
        abort(403)
    else:
        # If user exists, destroy their session
        AUTH.destroy_session(user.id)
        # Redirect to GET /
        return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
