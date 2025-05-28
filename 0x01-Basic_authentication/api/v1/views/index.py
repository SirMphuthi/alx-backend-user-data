#!/usr/bin/env python3
"""
Module of Index views.
"""
from flask import jsonify, abort  # Required Flask imports for views
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Returns:
      - The status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Returns:
      - The number of each object.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()  # Assuming User.count() is implemented
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def trigger_unauthorized():
    """
    GET /api/v1/unauthorized
    Triggers a 401 Unauthorized error.
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def trigger_forbidden():
    """
    GET /api/v1/forbidden
    Triggers a 403 Forbidden error.
    """
    abort(403)
