#!/usr/bin/env python3
"""DB module

This module defines the DB class for database operations related to
user authentication, including creating, finding, and updating users.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """
    DB class handles database operations for user authentication service.

    It manages the SQLAlchemy engine and session, providing methods
    to interact with the database (add, find, update users).
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance.

        Sets up SQLAlchemy engine for a SQLite database file 'a.db'.
        Drops and creates all tables defined by Base metadata.
        The session attribute is initialized to None.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.

        Returns a SQLAlchemy Session instance. Creates it if not existing.
        Ensures only one session is created per DB instance.
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
            User: The newly created User object after it is persisted,
                  with its `id` populated.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)
        return new_user

    def find_user_by(self, **kwargs: str) -> User:
        """
        Finds a user in the database based on arbitrary keyword arguments.

        Queries the 'users' table, returns the first matching row.

        Args:
            **kwargs: Keyword arguments for User model attributes (e.g.,
                      'email', 'session_id') and filter values.

        Returns:
            User: The first User object matching the arguments.

        Raises:
            NoResultFound: If no user found matching criteria.
            InvalidRequestError: If invalid attribute in kwargs.
        """
        return self._session.query(User).filter_by(**kwargs).one()

    def update_user(self, user_id: int, **kwargs: str) -> None:
        """
        Updates a user's attributes in the database.

        Locates user by ID via `find_user_by`, updates attributes from
        kwargs, and commits changes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: User attributes and their new values.

        Returns:
            None: Updates database in-place.

        Raises:
            NoResultFound: If user not found (propagated from `find_user_by`).
            ValueError: If an argument in kwargs is not a valid User attribute.
            InvalidRequestError: If invalid query argument (propagated).
        """
        user = self.find_user_by(id=user_id)

        valid_attributes = User.__table__.columns.keys()

        for key, value in kwargs.items():
            if key not in valid_attributes:
                raise ValueError(f"Invalid user attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
