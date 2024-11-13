#!/usr/bin/env python3
"""
Basic Auth module for API management
"""

from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64
import binascii


class BasicAuth(Auth):
    """
    BasicAuth class for handling Basic Authentication
    """

    def extract_b64_auth_header(self, auth_header: str) -> str:
        """
        Extracts the Base64 part from the Authorization header.
        Returns None if invalid.
        """
        if (auth_header is None or
                not isinstance(auth_header, str) or
                not auth_header.startswith("Basic")):
            return None
        return auth_header[6:]

    def decode_b64_auth_header(self, b64_auth_header: str) -> str:
        """
        Decodes the Base64 encoded string.
        Returns None if decoding fails.
        """
        if b64_auth_header and isinstance(b64_auth_header, str):
            try:
                encoded = b64_auth_header.encode('utf-8')
                decoded = base64.b64decode(encoded)
                return decoded.decode('utf-8')
            except binascii.Error:
                return None

    def extract_user_creds(self, decoded_b64_auth_header: str) -> (str, str):
        """
        Extracts the user email and password from the decoded Base64 string.
        Returns None, None if invalid.
        """
        if decoded_b64_auth_header and
               isinstance(decoded_b64_auth_header, str) and ":" in decoded_b64_auth_header:
            creds = decoded_b64_auth_header.split(":", 1)
            return creds[0], creds[1]
        return None, None

    def current_user(self, req=None) -> TypeVar('User'):
        """
        Retrieves the User instance from the request headers using Basic Auth.
        """
        auth_header = self.authorization_header(req)
        b64_header = self.extract_b64_auth_header(auth_header)
        decoded_header = self.decode_b64_auth_header(b64_header)
        user_creds = self.extract_user_creds(decoded_header)
        return self.user_object_from_credentials(*user_creds)
