#!/usr/bin/env python3
""" Module for Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a path requires authentication.
        Returns True if the path is not in the list of excluded_paths.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that don't require auth.
                                        Assumed to end with a '/'.
        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with a slash for consistent comparison
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Assuming excluded_path always ends with a '/'
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Retrieves the Authorization header from the request
        Args:
            request: The Flask request object.
        Returns:
            str: Always None for now.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the current user from the request
        Args:
            request: The Flask request object.
        Returns:
            TypeVar('User'): Always None for now.
        """
        return None
