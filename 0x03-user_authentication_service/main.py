#!/usr/bin/env python3
"""End-to-end integration test.
"""
import requests

BASE_URL = "http://localhost:5000"  # Adjust this URL to your app's base URL


def register_user(email: str, password: str) -> None:
    """Tests user registration."""
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests logging in with wrong password."""
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 401
    assert res.json() == {"message": "Incorrect password"}


def log_in(email: str, password: str) -> str:
    """Tests logging in."""
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """Tests accessing profile without logging in."""
    url = "{}/profile".format(BASE_URL)
    res = requests.get(url)
    assert res.status_code == 403
    assert res.json() == {"message": "Please log in first"}


def profile_logged(session_id: str) -> None:
    """Tests accessing profile after logging in."""
    url = "{}/profile".format(BASE_URL)
    cookies = {'session_id': session_id}
    res = requests.get(url, cookies=cookies)
    assert res.status_code == 200
    assert res.json() == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """Tests logging out."""
    url = "{}/sessions".format(BASE_URL)
    cookies = {'session_id': session_id}
    res = requests.delete(url, cookies=cookies)
    assert res.status_code == 200
    assert res.json() == {"message": "logged out"}


def reset_password_token(email: str) -> str:
    """Tests resetting password and getting the reset token."""
    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    res = requests.post(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "reset password"}
    return res.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests updating the password using the reset token."""
    url = "{}/reset_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    res = requests.put(url, data=body)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
