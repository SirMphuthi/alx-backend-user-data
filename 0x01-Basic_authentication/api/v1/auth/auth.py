#!/usr/bin/env python3
"""
Auth class to manage API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class definition.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a given path requires authentication.
        Returns True if the path is not in the list of excluded_paths.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Normalize path: ensure it has exactly one trailing slash
        if path == "/":
            normalized_path = "/"
        else:
            # Strip all trailing slashes, then add one back
            normalized_path = path.rstrip('/') + '/'

        for excluded_path_candidate in excluded_paths:
            # Defensive check for non-string or None elements
            if not isinstance(excluded_path_candidate, str) or \
                    excluded_path_candidate is None:
                continue

            # Normalize the excluded path candidate for consistent comparison
            if excluded_path_candidate == "/":
                normalized_excluded_path = "/"
            else:
                # THIS LINE IS NOW BROKEN INTO TWO FOR PEP8 COMPLIANCE
                normalized_excluded_path = \
                    excluded_path_candidate.rstrip('/') + '/'

            if normalized_path == normalized_excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header.
        """
        if request is None:
            return None

        # Check for header existence.
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user.
        Returns None for now.
        """
        return None
