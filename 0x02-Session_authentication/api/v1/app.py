#!/usr/bin/env python3
"""
API route module for managing user authentication and requests.
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.basic_auth import BasicAuth
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Determine the authentication mechanism based on the environment variable
auth_mech = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "auth":
    auth_mech = Auth()
elif auth_type == "basic_auth":
    auth_mech = BasicAuth()
elif auth_type == "session_auth":
    auth_mech = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth_mech = SessionExpAuth()
elif auth_type == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth_mech = SessionDBAuth()


@app.errorhandler(404)
def handle_not_found(error) -> str:
    """
    Handler for 404 Not Found error.
    Returns a JSON response indicating the resource was not found.
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def handle_unauthorized(error) -> str:
    """
    Handler for 401 Unauthorized error.
    Returns a JSON response indicating the user is not authenticated.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def handle_forbidden(error) -> str:
    """
    Handler for 403 Forbidden error.
    Returns a JSON response indicating access is restricted.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def check_request_authentication() -> None:
    """
    Check if a request requires authentication and handle accordingly.
    """
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/',
        '/api/v1/auth_session/login/'
    ]

    # Apply authentication if enabled and the path is not excluded
    if auth_mech and auth_mech.require_auth(request.path, excluded_paths):
        if auth_mech.authorization_header(request) is None and auth_mech.session_cookie(request) is None:
            abort(401)  # Unauthorized
        request.current_user = auth_mech.current_user(request)
        if request.current_user is None:
            abort(403)  # Forbidden


if __name__ == "__main__":
    server_host = getenv("API_HOST", "0.0.0.0")
    server_port = getenv("API_PORT", "5000")
    app.run(host=server_host, port=server_port)
