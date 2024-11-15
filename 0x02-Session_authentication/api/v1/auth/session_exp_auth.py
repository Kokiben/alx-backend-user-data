#!/usr/bin/env python3
"""
Session Expiration Authentication Class.
"""
from os import getenv
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Handles session expiration for authentication."""

    def __init__(self):
        """Initializes session duration from environment variable."""
        try:
            session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """Creates a new session ID with a timestamp.

        Args:
            user_id (str): ID of the user for whom the session is created.

        Returns:
            str: Session ID, or None if session creation fails.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        # Stores the user ID with the session creation timestamp
        session_info = {'user_id': user_id, 'created_at': datetime.now()}
        SessionAuth.user_id_by_session_id[session_id] = session_info
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user ID if the session is valid and not expired.

        Args:
            session_id (str): The session ID to validate.

        Returns:
            str: User ID associated with the session if valid, otherwise None.
        """
        if session_id is None:
            return None
        if session_id not in SessionAuth.user_id_by_session_id:
            return None
        
        session_info = SessionAuth.user_id_by_session_id[session_id]
        
        # If session duration is zero or less, return user_id
        if self.session_duration <= 0:
            return session_info["user_id"]
        
        # Validates expiration by checking the timestamp
        if "created_at" not in session_info:
            return None
        create_time = session_info["created_at"]
        expiration_period = timedelta(seconds=self.session_duration)
        
        # Returns None if session has expired, else user_id
        if (create_time + expiration_period) < datetime.now():
            return None
        return session_info["user_id"]
