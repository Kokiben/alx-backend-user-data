#!/usr/bin/env python3
"""
API route module with authentication and error handling.
"""
from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import logging

# Initialize Flask application and CORS
application = Flask(__name__)
application.register_blueprint(app_views)
CORS(application, resources={r"/api/v1/*": {"origins": "*"}})

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("api")

# Select authentication type based on environment variable
authentication = None
auth_type = getenv("AUTH_TYPE")

if auth_type == "auth":
    authentication = Auth()
elif auth_type == "basic_auth":
    authentication = BasicAuth()

log.info(f"Authentication type set to: {auth_type or 'None'}")


@application.errorhandler(404)
def handle_404(error) -> str:
    """ Handler for 404 Not Found """
    return jsonify({"error": "Not found"}), 404


@application.errorhandler(401)
def handle_401(error) -> str:
    """ Handler for 401 Unauthorized """
    return jsonify({"error": "Unauthorized"}), 401


@application.errorhandler(403)
def handle_403(error) -> str:
    """ Handler for 403 Forbidden """
    return jsonify({"error": "Forbidden"}), 403


@application.before_request
def pre_request_handler():
    """
    Handler to run before processing each request.
    """
    un_pth = ['/api/v1/status', '/api/v1/unauthorized/', '/api/v1/forbidden']
    log.info(f"Request path: {request.path}")

    # Check if authentication is required for the requested path
    if authentication and authentication.require_auth(request.path, un_pth):
        if not authentication.authorization_header(request):
            log.warning(f"Unauthorized access attempt on {request.path}")
            abort(401)
        request.current_user = authentication.current_user(request)  # Assign current user
        if not request.current_user:
            log.warning(f"Forbidden access attempt on {request.path}")
            abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    application.run(host=host, port=port)
