#!/usr/bin/env python3
"""
Auth class for managing API authentication.
"""

import fnmatch
from flask import request
from typing import TypeVar, List

User = TypeVar('User')


class Auth:
    """
    A class to manage API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns False if the path matches any in excluded_paths.
        Handles trailing tolerance and wildcard matching for excluded paths.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize the path by removing trailing slashes
        normalized_path = path.rstrip('/')

        # Check if the path matches any excluded path
        for excluded_path in excluded_paths:
            # Normalize the excluded path and allow wildcard matching
            normalized_excluded_path = excluded_path.rstrip('/')
            if fnmatch.fnmatch(normalized_path, normalized_excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the 'Authorization' header from the request
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """
        Retrieves the current user based on the request.
        Checks for a Bearer token in the 'Authorization' header, or cookie.
        """
        # First, check for an 'Authorization' header
        auth_header = self.authorization_header(request)
        if auth_header:
            # If a Bearer token is present, extract and return the user based
            match = re.match(r"^Bearer (\S+)$", auth_header)
            if match:
                token = match.group(1)
                # Here, you would typically validate the token and extract
                # For now, returning a mock user based on the token
                return f"User:{token}"  # Replace with actual

        # If no Bearer token, check for the 'user' cookie
        if request and 'user' in request.cookies:
            return request.cookies['user']

        return None
