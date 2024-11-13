#!/usr/bin/env python3
"""
Auth class
"""

from typing import List
import fnmatch


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns True if the path is not in the excluded_paths.
        Handles slash tolerance by ensuring paths with or a trailing slash
        are treated as equivalent.
        Also handles wildcard * at the end of excluded paths.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        # Normalize path by removing any trailing slashes for comparison
        normalized_path = path.rstrip('/')
        # Check against each excluded path
        for excluded_path in excluded_paths:
            # Normalize excluded path and match with wildcard support
            normalized_excluded_path = excluded_path.rstrip('/')
            if fnmatch.fnmatch(normalized_path, normalized_excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from the request.
        If no authorization header is present, returns None.
        """
        if request and 'Authorization' in request.headers:
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> str:
        """
        Returns the current user based on the request.
        If no user is found, returns None.
        This can be expanded to use a session or token-based system.
        """
        # Checking for 'Authorization' header (for token-based auth)
        auth_header = self.authorization_header(request)
        if auth_header:
            # Check if the Authorization header contains a Bearer token
            match = re.match(r"^Bearer (\S+)$", auth_header)
            if match:
                token = match.group(1)
                # Here you can add logic to validate token and extract user
                # For now, we're returning a mock user based ontoken
                return f"User:{token}"
        # Check cookies for a user if no Bearer token is found
        if request and 'user' in request.cookies:
            return request.cookies['user']
        return None
