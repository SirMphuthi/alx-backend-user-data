#!/usr/bin/env python3
"""
BasicAuth class for Basic Authentication
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class inherits from Auth.
    Extends Auth with methods specific to Basic Authentication.
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        Extracts the Base64 encoded part of the Authorization header
        for Basic Authentication.

        Args:
            authorization_header (str): The value of the Authorization header.

        Returns:
            str: The Base64 encoded part, or None if conditions are not met.
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        # Check if the header starts with "Basic " (note the space after Basic)
        if not authorization_header.startswith("Basic "):
            return None

        # Return the value after "Basic "
        # "Basic " has 6 characters, so slice from index 6 onwards.
        return authorization_header[len("Basic "):]
