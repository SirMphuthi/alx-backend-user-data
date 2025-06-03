#!/usr/bin/env python3
"""
Authentication module.

This module provides utilities for user authentication, including
password hashing functions using bcrypt.
"""
import bcrypt


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
    # Generate a random salt for bcrypt hashing
    salt = bcrypt.gensalt()

    # Hash the password. bcrypt.hashpw requires both password and salt
    # to be bytes, so encode the input password string.
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password
