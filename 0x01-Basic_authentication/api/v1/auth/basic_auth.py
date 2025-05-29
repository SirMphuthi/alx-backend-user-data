#!/usr/bin/env python3
"""
BasicAuth class for Basic Authentication
"""
import base64
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

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decodes a Base64 string to a UTF-8 string.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded UTF-8 string, or None if input is invalid or
                 decoding fails.
        """
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string. base64.b64decode expects bytes,
            # so encode the input string to bytes first.
            # Then decode the result to a UTF-8 string.
            decoded_bytes = base64.b64decode(
                base64_authorization_header.encode('utf-8')
            )
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            # Catch errors during Base64 decoding or UTF-8 decoding
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extracts the user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str): The decoded string
            (e.g., "email:password").

        Returns:
            tuple: A tuple containing (user_email, user_password),
                   or (None, None) if conditions are not met.
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        # Split the string at the first occurrence of ':'
        # (Assuming only one ':' as per requirement)
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
