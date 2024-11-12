#!/usr/bin/env python3
"""
Main application module for the API
"""

from flask import Flask, jsonify
from api.v1.views import index

app = Flask(__name__)

# Error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({"error": "Forbidden"}), 403

# Register Blueprint for index view
app.register_blueprint(index)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
