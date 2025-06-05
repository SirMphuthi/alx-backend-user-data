#!/usr/bin/env python3
"""
User views module
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users() -> str:
    """ GET /api/v1/users
    Return all users
    """
    users = [user.to_json() for user in User.all()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str) -> str:
    """ GET /api/v1/users/<user_id>
    Return one user
    """
    # New logic for /users/me
    if user_id == "me":
        # If user_id is 'me' but no current user is authenticated
        if not hasattr(request, 'current_user') or request.current_user is None:
            abort(404)  # 404 as if the specific user ID doesn't exist
        else:
            # If current_user is authenticated, return their JSON
            return jsonify(request.current_user.to_json())

    # Existing logic for normal user_id (UUID)
    try:
        user = User.get(user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_json())
    except Exception:
        # Catch potential errors if user_id is not a valid UUID format
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str) -> str:
    """ DELETE /api/v1/users/<user_id>
    Delete one user
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users
    Create a new user
    """
    try:
        r = request.get_json()
    except Exception:
        r = None
    if r is None:
        return jsonify({"error": "Wrong format"}), 400
    if "email" not in r:
        return jsonify({"error": "email missing"}), 400
    if "password" not in r:
        return jsonify({"error": "password missing"}), 400
    try:
        user = User()
        user.email = r["email"]
        user.password = r["password"]
        user.first_name = r.get("first_name")
        user.last_name = r.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({"error": "Can't create User: {}".format(e)}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str) -> str:
    """ PUT /api/v1/users/<user_id>
    Update one user
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    try:
        r = request.get_json()
    except Exception:
        r = None
    if r is None:
        return jsonify({"error": "Wrong format"}), 400
    for name, value in r.items():
        if name not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, name, value)
    user.save()
    return jsonify(user.to_json()), 200
