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
    # Assuming User.count() is correctly implemented, otherwise it will be 0
    stats['users'] = User.count() if hasattr(User, 'count') else 0
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def trigger_unauthorized():
    """ GET /api/v1/unauthorized
    Return:
      - Triggers a 401 Unauthorized error
    """
    # This will immediately raise a 401 error, handled by app.py
    abort(401)


# --- NEW: Endpoint to trigger a 403 Forbidden error ---
@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def trigger_forbidden():
    """ GET /api/v1/forbidden
    Return:
      - Triggers a 403 Forbidden error
    """
    # This will immediately raise a 403 error, handled by app.py
    abort(403)
