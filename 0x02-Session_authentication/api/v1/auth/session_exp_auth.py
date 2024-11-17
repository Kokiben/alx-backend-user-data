#!/usr/bin/env python3
"""Create a class SessionExpAuth
"""
import os
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Handles session-based authentication with expiration.
    """

    def __init__(self) -> None:
        """Initialize session expiration duration.
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session with expiration details.
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Get user ID for a valid session.
        """
        if session_id in self.user_id_by_session_id:
            sessi_dct = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return sessi_dct['user_id']
            if 'created_at' not in sessi_dct:
                return None
            cr_tm = datetime.now()
            tm_sp = timedelta(seconds=self.session_duration)
            ex_tm = sessi_dct['created_at'] + tm_sp
            if ex_tm < cr_tm:
                return None
            return sessi_dct['user_id']
