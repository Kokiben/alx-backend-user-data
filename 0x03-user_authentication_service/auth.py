#!/usr/bin/env python3
"""Authentication module for managing user authentication routines.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generates a unique UUID as a string.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user if the email is not already in use.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials.
        """
        ur = None
        try:
            ur = self._db.find_user_by(email=email)
            if ur is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    ur.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Creates a new session for the user and returns the session ID.
        """
        ur = None
        try:
            ur = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if ur is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(ur.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get a user associated with the given session ID.
        """
        ur = None
        if session_id is None:
            return None
        try:
            ur = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return ur

    def destroy_session(self, user_id: int) -> None:
        """Removes the session ID for a given user.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a password reset token for the user.
        """
        ur = None
        try:
            ur = self._db.find_user_by(email=email)
        except NoResultFound:
            ur = None
        if ur is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(ur.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password using the provided reset token.
        """
        ur = None
        try:
            ur = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            ur = None
        if ur is None:
            raise ValueError()
        nw_passwd_hsh = _hash_password(password)
        self._db.update_user(
            ur.id,
            hashed_password=nw_passwd_hsh,
            reset_token=None,
        )
