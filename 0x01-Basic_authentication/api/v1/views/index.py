#!/usr/bin/env python3
""" Index View module
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def fetch_status() -> str:
    """ 
    GET /api/v1/status
    Response:
      - Returns the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def fetch_statistics() -> str:
    """ 
    GET /api/v1/stats
    Response:
      - Returns the count of each object (e.g., users).
    """
    from models.user import User
    object_counts = {}
    object_counts['users'] = User.count()
    return jsonify(object_counts)


@app_views.route('/unauthorized', strict_slashes=False)
def initiate_unauthorized() -> str:
    """ 
    GET /api/v1/unauthorized
    Action:
      - Aborts the request with a 401 Unauthorized error.
    """
    abort(401)


@app_views.route('/forbidden', strict_slashes=False)
def initiate_forbidden() -> str:
    """ 
    GET /api/v1/forbidden
    Action:
      - Aborts the request with a 403 Forbidden error.
    """
    abort(403)
