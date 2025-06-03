#!/usr/bin/env python3
"""
Basic Flask app module.

This module sets up a simple Flask web application with a single
GET route ('/') that returns a JSON welcome message.
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> dict:
    """
    GET /

    Returns a JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
