#!/usr/bin/env python3
"""
Authentication module.

This module provides utilities for user authentication, including
password hashing functions and user registration/login management.
"""
import bcrypt
from db import DB
from user import User  # Import User for type hinting the return type
from sqlalchemy.orm.exc import NoResultFound  # To catch when user is not found


def _hash_password(password: str) -> bytes:
    """
    Hashes a plain-text password string using bcrypt.

    This function generates a salt and then uses bcrypt.hashpw to create
    a salted hash of the input password.

    Args:
        password (str): The plain-text password string to hash.

    Returns:
        bytes: The salted and hashed password as bytes.
               The hash includes the salt and the cost factor,
               suitable for storage.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.

    Manages user registration, login, and session handling by
    interacting with the DB class.
    """

    def __init__(self) -> None:
        """
        Initializes an Auth instance.

        Sets up a private database connection instance using the DB class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user in the database.

        Checks if a user with the provided email already exists. If so,
        it raises a ValueError. Otherwise, it hashes the password,
        saves the new user to the database, and returns the User object.

        Args:
            email (str): The email address of the user to register.
            password (str): The plain-text password for the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        try:
            # Attempt to find user by email. If found, it means the email
            # is already registered.
            self._db.find_user_by(email=email)
            # If find_user_by succeeds (i.e., doesn't raise NoResultFound),
            # then a user with this email already exists.
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If NoResultFound is raised, the user does not exist,
            # and we can proceed with registration.
            pass

        # Hash the plain-text password
        hashed_password = _hash_password(password)

        # Save the new user to the database
        user = self._db.add_user(email, hashed_password)

        # Return the newly created User object
        return user
