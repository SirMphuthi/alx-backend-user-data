#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort # Ensure 'abort' is imported here
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count() # Assuming User.count() is correctly implemented
    return jsonify(stats)


# --- New endpoint for the unauthorized error handler ---
@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def trigger_unauthorized():
    """ GET /api/v1/unauthorized
    Return:
      - Triggers a 401 Unauthorized error
    """
    abort(401) # This will raise the 401 error, handled by app.py


# --- Endpoint for the forbidden error handler (from a later task, keep for continuity) ---
@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def trigger_forbidden():
    """ GET /api/v1/forbidden
    Return:
      - Triggers a 403 Forbidden error
    """
    abort(403)
