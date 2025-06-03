#!/usr/bin/env python3
"""
Authentication module.

Manages user authentication: hashing, registration, login.
"""
import bcrypt
import uuid  # Import the uuid module
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a password with bcrypt.

    Args:
        password (str): Plain-text password.

    Returns:
        bytes: Salted, hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Generates a new UUID.

    Returns:
        str: String representation of a new UUID (UUID4 standard).
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class for database interaction.

    Handles user registration and login.
    """

    def __init__(self) -> None:
        """
        Initializes Auth instance.

        Sets up private database connection.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user.

        Args:
            email (str): User's email.
            password (str): User's password.

        Returns:
            User: The new User object.

        Raises:
            ValueError: If user email exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user login.

        Checks email existence and password match.

        Args:
            email (str): User email.
            password (str): User password.

        Returns:
            bool: True if login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False
