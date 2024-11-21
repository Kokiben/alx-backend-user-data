#!/usr/bin/env python3
"""A Flask app for user authentication.
"""
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def hi_world() -> str:
    """Home route.
    Return:
        - JSON welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_us() -> str:
    """Register a new user.
    Return:
        - JSON response with user creation status.
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Log in a user and create a session.
    Return:
        - JSON response with login status and session ID.
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    rspn = jsonify({"email": email, "message": "logged in"})
    rspn.set_cookie("session_id", session_id)
    return rspn


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """Log out a user by destroying the session.
    Return:
        - Redirect to the home route.
    """
    session_id = request.cookies.get("session_id")
    ur = AUTH.get_user_from_session_id(session_id)
    if ur is None:
        abort(403)
    AUTH.destroy_session(ur.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """Retrieve the user's profile.
    Return:
        - JSON response with user email.
    """
    session_id = request.cookies.get("session_id")
    ur = AUTH.get_user_from_session_id(session_id)
    if ur is None:
        abort(403)
    return jsonify({"email": ur.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """Generate a password reset token.
    Return:
        - JSON response with reset token.
    """
    email = request.form.get("email")
    rst_tokn = None
    try:
        rst_tokn = AUTH.get_reset_password_token(email)
    except ValueError:
        rst_tokn = None
    if rst_tokn is None:
        abort(403)
    return jsonify({"email": email, "reset_token": rst_tokn})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """Update the user's password using a reset token.

    Return:
        - JSON response with status message.
    """
    email = request.form.get("email")
    rst_tokn = request.form.get("reset_token")
    nw_passwd = request.form.get("new_password")
    Is_passwd = False
    try:
        AUTH.update_password(rst_tokn, nw_passwd)
        Is_passwd = True
    except ValueError:
        Is_passwd = False
    if not Is_passwd:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
