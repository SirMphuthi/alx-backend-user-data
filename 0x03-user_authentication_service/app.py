#!/usr/bin/env python3
"""
Basic Flask app module.

This module sets up a simple Flask web application with a single
GET route that returns a JSON welcome message, and a POST route
for user registration.
"""
from flask import Flask, jsonify, request
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

    Expects 'email' and 'password' as form fields.
    If the user does not exist, registers them and responds with:
    {"email": "<registered email>", "message": "user created"} (200 OK).
    If the user is already registered, responds with:
    {"message": "email already registered"} (400 BAD REQUEST).

    Returns:
        tuple: A Flask response (JSON payload, HTTP status code).
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        # Attempt to register the user using the AUTH instance
        user = AUTH.register_user(email, password)
        # If successful, return the success message with email and 200 status
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # If register_user raises ValueError (due to existing user),
        # return the error message with 400 status
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
