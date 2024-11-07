#!/usr/bin/env python3
"""
Password encryption and validation
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash the password with bcrypt and return the salted hash """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check if the provided password matches the hashed password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
