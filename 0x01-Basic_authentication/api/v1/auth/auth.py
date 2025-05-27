#!/usr/bin/env python3
""" Module for Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class to manage API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a path requires authentication
        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that don't require auth.
        Returns:
            bool: Always False for now.
        """
        return False

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
