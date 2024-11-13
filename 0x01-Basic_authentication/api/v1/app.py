#!/usr/bin/env python3
"""
API route module.
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
authenticator = None

# Set the authentication method based on environment variable
if getenv("AUTH_TYPE") == "auth":
    authenticator = Auth()
elif getenv("AUTH_TYPE") == "basic_auth":
    authenticator = BasicAuth()


@app.errorhandler(404)
def handle_not_found(error) -> str:
    """
    Handle 404 errors (Not Found).
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def handle_unauthorized(error) -> str:
    """
    Handle 401 errors (Unauthorized).
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def handle_forbidden(error) -> str:
    """
    Handle 403 errors (Forbidden).
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def pre_request_handler():
    """
    Handle actions before processing the request.
    """
    public_routes = [
        '/api/v1/status',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden'
    ]

    requires_auth = (
        authenticator and
        authenticator.require_auth(request.path, public_routes)
    )

    if requires_auth:
        if not authenticator.authorization_header(request):
            abort(401)
        if not authenticator.current_user(request):
            abort(403)


if __name__ == "__main__":
    api_host = getenv("API_HOST", "0.0.0.0")
    api_port = getenv("API_PORT", "5000")
    app.run(host=api_host, port=api_port)
