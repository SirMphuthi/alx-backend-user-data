#!/usr/bin/env python3
"""
Module for basic authentication.
"""
from flask import request
from typing import List, TypeVar, Union
from models.user import User


class Auth:
    """
    Auth class for managing authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.

        Args:
            path (str): The request path.
            excluded_paths (List[str]): A list of paths that do not
                                        require authentication.

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
            if excluded_path.endswith('*'):
                # Wildcard match (e.g., /admin/* matches /admin/dashboard)
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                # Exact match
                return False
        return True

    def authorization_header(self, request=None) -> Union[str, None]:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            Union[str, None]: The value of the Authorization header,
                              or None if not present.
        """
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> Union[User, None]:
        """
        Retrieves the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            Union[User, None]: The User object if authenticated,
                              otherwise None.
        """
        return None  # To be implemented in future tasks
