#!/usr/bin/env python3
"""Module for session authentication views.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


@app_views.route(
    '/auth_session/login', methods=['POST'], strict_slashes=False)
def ses_ion_login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    Returns:
      - JSON representation of the authenticated User object.
    """
    error_response = {"error": "no user found for this email"}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        user_list = User.search({'email': email})
    except Exception:
        return jsonify(error_response), 404
    if len(user_list) <= 0:
        return jsonify(error_response), 404
    if user_list[0].is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(getattr(user_list[0], 'id'))
        response = jsonify(user_list[0].to_json())
        response.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return response
    return jsonify({"error": "wrong password"}), 401

@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def ses_ion_logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Returns:
      - An empty JSON object to confirm logout.
    """
    from api.v1.app import auth
    session_destroyed = auth.destroy_session(request)
    if not session_destroyed:
        abort(404)
    return jsonify({})
