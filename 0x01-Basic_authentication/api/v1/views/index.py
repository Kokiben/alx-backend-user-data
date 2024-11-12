#!/usr/bin/env python3
"""
Route module for the API
"""

from flask import Blueprint, abort

index = Blueprint('index', __name__)

@index.route('/api/v1/forbidden', methods=['GET'])
def forbidden():
    abort(403)  # This will trigger the 403 error handler in app.py
