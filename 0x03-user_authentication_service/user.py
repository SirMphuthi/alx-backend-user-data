#!/usr/bin/env python3
"""
SQLAlchemy User model for the 'users' database table.

This module defines the User class, which maps to the 'users' table
in the database, specifying its columns and their types.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """
    User model for the 'users' database table.

    This class defines the schema for the users table with the following
    attributes: id (primary key), email, hashed_password, session_id,
    and reset_token. It uses SQLAlchemy's declarative base for mapping.
    """
    __tablename__ = 'users'

    id: Column = Column(Integer, primary_key=True)
    email: Column = Column(String(250), nullable=False)
    hashed_password: Column = Column(String(250), nullable=False)
    session_id: Column = Column(String(250), nullable=True)
    reset_token: Column = Column(String(250), nullable=True)

    # Note on type annotations for attributes:
    # While attributes like 'id', 'email' etc. are defined,
    # SQLAlchemy's declarative system handles their creation.
    # The requirement "All your functions should be type annotated" applies
    # to methods (functions) defined within the class or module.
    # Since no custom __init__ or other methods are explicitly defined here,
    # no function-level type annotations are necessary for this specific task.
