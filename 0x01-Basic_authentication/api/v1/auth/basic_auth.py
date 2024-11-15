#!/usr/bin/env python3
"""
basic Authentication module for handling user authentication.
"""

from api.v1.auth.auth import Auth
from typing import TypeVar, List
from models.user import User
import base64
import binascii


class BasicAuth(Auth):
    """
    basicAuth class for implementing Basic Authentication methods.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        return Base64 encoded part of the header, or None if invalid.
        header The authorization header string.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        hadr_arr = authorization_header.split(" ")
        if hadr_arr[0] != "Basic":
            return None
        else:
            return hadr_arr[1]
        # use authorization_header
        # and extract_base64_authorization_header 
        # and decode_base64_authorization_header
        # and extract_user_credentials

        # and user_object_from_credentials

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns The decoded string, or None if decoding fails.
        The Base64 encoded string.
        """
        bs64_ath_hadr = base64_authorization_header
        if bs64_ath_hadr and isinstance(bs64_ath_hadr, str):
            try:
                ecod = bs64_ath_hadr.encode('utf-8')
                bs = base64.b64decode(ecod)
                return bs.decode('utf-8')
            except binascii.Error:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns tuple with email and password, or (None, None) if invalid.
        """
        dcodd_bs64 = decoded_base64_authorization_header
        if (dcodd_bs64 and isinstance(dcodd_bs64, str) and
                ":" in dcodd_bs64):
            credential = dcodd_bs64.split(":", 1)
            return (credential[0], credential[1])
        return (None, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the authenticated user based on the request."""

        Ath_hadr = self.authorization_header(request)
        if Ath_hadr is not None:
            tkn = self.extract_base64_authorization_header(Ath_hadr)
            if tkn is not None:
                dcodd = self.decode_base64_authorization_header(tkn)
                if dcodd is not None:
                    email, pwod = self.extract_user_credentials(dcodd)
                    if email is not None:
                        return self.user_object_from_credentials(email, pwod)
        return

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Validates user credentials and returns the corresponding User object.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            Usrs = User.search({'email': user_email})
            if not Usrs or Usrs == []:
                return None
            for Us in Usrs:
                if Us.is_valid_password(user_pwd):
                    return Us
            return None
        except Exception:
            return None
