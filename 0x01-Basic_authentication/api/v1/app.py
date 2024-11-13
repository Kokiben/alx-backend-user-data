#!/usr/bin/env python3
"""
Module for managing API routes and authentication.
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth_system = None

# Load the appropriate authentication system based on the environment
if getenv("AUTH_TYPE") == "auth":
    auth_system = Auth()
elif getenv("AUTH_TYPE") == "basic_auth":
    auth_system = BasicAuth()


@app.errorhandler(404)
def resource_not_found(error) -> str:
    """ Handles 404 Not Found errors """
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(401)
def unauthorized_access(error) -> str:
    """ Handles 401 Unauthorized access errors """
    return jsonify({"error": "Unauthorized access"}), 401


@app.errorhandler(403)
def forbidden_access(error) -> str:
    """ Handles 403 Forbidden access errors """
    return jsonify({"error": "Forbidden access"}), 403


@app.before_request
def authenticate_request():
    """
    Pre-request handler that checks if the route requires authentication.
    If the path is not in the public paths list, authentication is enforced.
    """
    exempt_paths = ['/api/v1/status/',
                    '/api/v1/unauthorized/', '/api/v1/forbidden/']

    # If auth is enabled and the route requires authentication
    if auth_system and auth_system.require_auth(request.path, exempt_paths):
        if not auth_system.authorization_header(request):
            abort(401)  # Unauthorized if no authorization
        if not auth_system.current_user(request):
            abort(403)  # Forbidden if no valid user is found


if __name__ == "__main__":
    # Start the app using host and port from environment variables
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
