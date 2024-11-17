#!/usr/bin/env python3
"""Session authentication with expiration and storage.
"""
from flask import request
from datetime import datetime, timedelta
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Handles session authentication with expiration and storage.
    """

    def create_session(self, user_id=None) -> str:
        """Create and save a session.
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            usr_sessi = UserSession(**kwargs)
            usr_sessi.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user ID for a session.
        """
        try:
            sessi = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessi) <= 0:
            return None
        cr_tm = datetime.now()
        tm_sp = timedelta(seconds=self.session_duration)
        ex_tm = sessi[0].created_at + tm_sp
        if ex_tm < cr_tm:
            return None
        return sessi[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroy a session.
        """
        session_id = self.session_cookie(request)
        try:
            sessi = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessi) <= 0:
            return False
        sessi[0].remove()
        return True
