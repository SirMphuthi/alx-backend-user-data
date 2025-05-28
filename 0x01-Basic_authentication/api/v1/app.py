#!/usr/bin/python3
"""
Main Flask application
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)

# --- CORS configuration (if applicable, often part of standard setup) ---
# Example: If your project uses Flask-CORS, you might have something like this:
# from flask_cors import CORS
# CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


# --- Authentication instance initialization ---
auth = None
# Get AUTH_TYPE environment variable to determine which auth method to use
AUTH_TYPE = os.getenv('AUTH_TYPE')

if AUTH_TYPE == 'auth':
    # Import Auth class only if AUTH_TYPE is 'auth'
    from api.v1.auth.auth import Auth
    auth = Auth()
# (e.g., if AUTH_TYPE == 'basic_auth', 'session_auth', etc.)

# --- 3. Define error handlers for the app ---


@app.errorhandler(401)
def unauthorized(error):
    """ Handler for 401 Unauthorized errors
    Returns a JSON response with status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401


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


# --- 4. Implement before_request handler ---
@app.before_request
def handle_before_request():
    """ Handles operations before each request is processed.
    This is where authentication and authorization checks occur.
    """
    # If no auth instance is configured, skip authentication checks
    # (e.g., if AUTH_TYPE is not 'auth' or not set)
    if auth is None:
        return

    # Define paths that explicitly do NOT require authentication
    # These are provided in the problem description.
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    # Check if the current request path requires authentication
    # This uses the auth.require_auth method for consistent slash handling
    if auth.require_auth(request.path, excluded_paths):
        # If authentication is required for this path:
        # 1. Check if the Authorization header is present
        if auth.authorization_header(request) is None:
            abort(401)

        # 2. Check if a current user can be identified
        # For now, current_user always returns None, effectively making any
        # request with an Authorization header lead to a 403
        if auth.current_user(request) is None:
            abort(403)

    # If auth is not required
    # (by simply returning None from before_request)


# --- 5. Main execution block for running the Flask development server ---
if __name__ == "__main__":
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))

    app.run(host=API_HOST, port=API_PORT, debug=True)
