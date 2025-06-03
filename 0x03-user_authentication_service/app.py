#!/usr/bin/env python3
"""
Basic Flask app module.

This module sets up a simple Flask web application with routes for
user registration and session management.
"""
from flask import Flask, jsonify, request, abort, make_response
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

    # Validate login credentials using the Auth class
    if not AUTH.valid_login(email, password):
        # If login is incorrect, respond with 401 Unauthorized
        abort(401)

    # If login is valid, create a new session for the user
    session_id = AUTH.create_session(email)

    # Prepare the JSON response payload
    response_data = {"email": email, "message": "logged in"}

    # Create a Flask response object to add the cookie
    response = make_response(jsonify(response_data))

    # Set the session_id as a cookie on the response
    response.set_cookie("session_id", session_id)

    return response, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
