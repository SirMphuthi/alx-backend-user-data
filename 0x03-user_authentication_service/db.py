#!/usr/bin/env python3
"""DB module

This module defines the DB class for handling database operations
related to user authentication, including creating and finding user records.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

# Import User model and Base from the user module
from user import Base, User


from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """
    DB class handles database operations for the user authentication service.

    It manages the SQLAlchemy engine and session, providing methods
    to interact with the database, such as adding new user records
    and finding existing ones based on various criteria.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance.

        Sets up the SQLAlchemy engine to connect to an in-memory SQLite DB
        named 'a.db'. It drops any existing tables defined by Base metadata
        and then creates all necessary tables.
        """
        # Using echo=False for cleaner output in production/testing
        self._engine = create_engine("sqlite:///a.db", echo=False)
        # Drop all existing tables (if any) defined by Base metadata
        Base.metadata.drop_all(self._engine)
        # Create all tables defined by Base metadata
        Base.metadata.create_all(self._engine)
        self.__session = None  # Initialize private session attribute

    @property
    def _session(self) -> Session:
        """
        Memoized session object.

        Returns a SQLAlchemy Session instance. If a session does not
        already exist for this DB instance, it creates a new one
        bound to the engine. This method ensures only one session
        is created per DB instance.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user record to the database.

        Args:
            email (str): The email address of the new user.
            hashed_password (str): The hashed password of the new user.

        Returns:
            User: The newly created User object after it has been
                  persisted to the database, with its `id` populated.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)
        return new_user

    def find_user_by(self, **kwargs: str) -> User:
        """
        Finds a user in the database based on arbitrary keyword arguments.

        This method queries the 'users' table and returns the first row
        that matches the provided criteria.

        Args:
            **kwargs: Arbitrary keyword arguments where keys are User model
                      attribute names (e.g., 'email', 'session_id') and
                      values are the desired filter values.

        Returns:
            User: The first User object found that matches all the
                  specified keyword arguments.

        Raises:
            NoResultFound: If no user is found in the database that matches
                           all the provided keyword arguments. This exception
                           is imported from `sqlalchemy.orm.exc`.
            InvalidRequestError: If one of the provided keyword arguments
                                 does not correspond to a valid attribute
                                 of the User model. This exception is
                                 imported from `sqlalchemy.exc`.
        """
        # Use _session.query(User) to start a query for User objects.
        # .filter_by(**kwargs) applies the keyword arguments as filters.
        # .one() attempts to retrieve exactly one result.
        # SQLAlchemy will automatically raise NoResultFound
        # based on the query outcome and validity of kwargs.
        return self._session.query(User).filter_by(**kwargs).one()
