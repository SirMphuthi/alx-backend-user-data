#!/usr/bin/env python3
"""
Authentication module.

Manages user authentication: hashing, registration, login, sessions.
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


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

    def create_session(self, email: str) -> str:
        """
        Creates a new session for a user.

        Finds user by email, generates new UUID (session ID), stores in DB.

        Args:
            email (str): Email of the user for whom to create a session.

        Returns:
            str: The newly generated session ID if the user is found,
                 otherwise None.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Retrieves a user based on their session ID.

        Args:
            session_id (str): The session ID string.

        Returns:
            Union[User, None]: The User object if found, otherwise None.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a user's session by setting their session ID to None.

        Args:
            user_id (int): The ID of the user whose session to destroy.
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a password reset token for a user.

        Finds the user by email, generates a UUID for the reset token,
        updates the user's reset_token in the database, and returns the token.

        Args:
            email (str): The email of the user.

        Returns:
            str: The newly generated reset token.

        Raises:
            ValueError: If the user with the provided email does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("Email not found")

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password using a reset token.

        Finds the user by reset token. If found, hashes the new password
        and updates the user's hashed_password and clears the reset_token.

        Args:
            reset_token (str): The reset token associated with the user.
            password (str): The new plain-text password.

        Raises:
            ValueError: If no user is found for the given reset token.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            # If user not found with the reset token, raise ValueError
            raise ValueError("Invalid reset token")

        # Hash the new password using the private helper function
        new_hashed_password = _hash_password(password)

        # Update the user's hashed_password and set reset_token to None
        self._db.update_user(
            user.id,
            hashed_password=new_hashed_password,
            reset_token=None
        )
