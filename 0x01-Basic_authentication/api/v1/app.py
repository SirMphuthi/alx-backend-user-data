#!/usr/bin/python3
"""
Main Flask application
"""
from flask import Flask, jsonify
from api.v1.views import app_views

# --- 1. Initialize the Flask app instance ---
app = Flask(__name__)

# --- 2. Register blueprints (like app_views) with the app ---
app.register_blueprint(app_views)

# --- 3. Define error handlers for the app ---
@app.errorhandler(401)
def unauthorized(error):
    """ Handler for 401 Unauthorized errors
    Returns a JSON response with status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401

# --- NEW: Handler for 403 Forbidden errors ---
@app.errorhandler(403)
def forbidden(error):
    """ Handler for 403 Forbidden errors
    Returns a JSON response with status code 403.
    """
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(404)
def not_found(error):
    """ Handler for 404 Not Found errors
    Returns a JSON response with status code 404.
    """
    return jsonify({"error": "Not found"}), 404

# --- 4. Main execution block for running the Flask development server ---
if __name__ == "__main__":
    import os

    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))

    app.run(host=API_HOST, port=API_PORT, debug=True)
