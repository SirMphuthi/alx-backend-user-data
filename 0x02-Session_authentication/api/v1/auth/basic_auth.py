#!/usr/bin/env python3
"""
Module for basic authentication.
"""
import base64 # Make sure this is imported if it wasn't
from api.v1.auth.auth import Auth
from models.user import User
# From typing import List, TypeVar, Union are already there for Auth class
from typing import Union, Tuple # <--- ADD 'Tuple' HERE


class BasicAuth(Auth):
    """
    BasicAuth class for basic authentication.
    Inherits from Auth.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> Union[str, None]:
        """
        Extracts the Base64 part of the Authorization header.

        Args:
            authorization_header (str): The full Authorization header.

        Returns:
            Union[str, None]: The Base64 part if it's a Basic header,
                              otherwise None.
        """
        if not authorization_header or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> Union[str, None]:
        """
        Decodes a Base64 string.

        Args:
            base64_authorization_header (str): The Base64 string to decode.

        Returns:
            Union[str, None]: The decoded string, or None on error.
        """
        if not base64_authorization_header or \
           not isinstance(base64_authorization_header, str):
            return None
        try:
            # Ensure it's padded correctly for base64.b64decode
            padding = len(base64_authorization_header) % 4
            if padding > 0:
                base64_authorization_header += "=" * (4 - padding)
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (Exception, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_authorization_header: str
                                 ) -> Tuple[str, str]: # <--- CHANGE 'tuple' to 'Tuple' here
        """
        Extracts user email and password from the decoded header.

        Args:
            decoded_authorization_header (str): The decoded "email:password" string.

        Returns:
            Tuple[str, str]: A tuple containing (email, password).
        """
        if not decoded_authorization_header or \
           not isinstance(decoded_authorization_header, str) or \
           ":" not in decoded_authorization_header:
            return (None, None)
        parts = decoded_authorization_header.split(":", 1)
        return (parts[0], parts[1])

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> Union[User, None]:
        """
        Retrieves a User object from email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's plain-text password.

        Returns:
            Union[User, None]: The User object if credentials are valid,
                              otherwise None.
        """
        if not user_email or not isinstance(user_email, str) or \
           not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users:
                return None
            user = users[0]
            if user.is_valid_password(user_pwd):
                return user
        except Exception:
            pass
        return None

    def current_user(self, request=None) -> Union[User, None]:
        """
        Retrieves the current user based on the Authorization header.

        Args:
            request: The Flask request object.

        Returns:
            Union[User, None]: The User object if authenticated via Basic Auth,
                              otherwise None.
        """
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        base64_header = self.extract_base64_authorization_header(
            authorization_header
        )
        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(
            base64_header
        )
        if decoded_header is None:
            return None

        email, password = self.extract_user_credentials(decoded_header)
        if email is None or password is None:
            return None

        return self.user_object_from_credentials(email, password)
