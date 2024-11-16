#!/usr/bin/env python3
""" Module that defines the index views and corresponding API endpoints.
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ Handles the GET request to /api/v1/status
    Returns:
      - A JSON response with the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ Handles the GET request to /api/v1/stats
    Returns:
      - A JSON response containing the count of various objects (e.g., users)
    """
    from models.user import User
    statistics = {}
    statistics['users'] = User.count()
    return jsonify(statistics)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ Handles the GET request to /api/v1/unauthorized
    Returns:
      - A 401 Unauthorized error
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """ Handles the GET request to /api/v1/forbidden
    Returns:
      - A 403 Forbidden error
    """
    abort(403)
