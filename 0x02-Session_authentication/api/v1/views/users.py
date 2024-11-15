#!/usr/bin/env python3
"""
User views module.
"""
from flask import jsonify, request, abort
from models.user import User
from api.v1.views import app_views

@app_views.route('/api/v1/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str) -> Tuple[str, int]:
    """ GET /api/v1/users/<user_id>
    Return:
      - JSON representation of a User object.
    """
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/api/v1/users/me', methods=['GET'], strict_slashes=False)
def get_current_user() -> Tuple[str, int]:
    """ GET /api/v1/users/me
    Return the current authenticated user.
    """
    if request.current_user is None:
        abort(404)
    return jsonify(request.current_user.to_json())
