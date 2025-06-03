#!/usr/bin/env python3
"""DB module

Handles database operations for user authentication service.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class DB:
    """
    DB class for user authentication database operations.

    Manages SQLAlchemy engine/session for user management.
    """

    def __init__(self) -> None:
        """
        Initialize DB instance.

        Connects to 'a.db' SQLite file. Drops/creates tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.

        Returns SQLAlchemy Session. Creates if not exists.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds new user.

        Args:
            email (str): User email.
            hashed_password (str): Hashed password.

        Returns:
            User: New User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)
        return new_user

    def find_user_by(self, **kwargs: str) -> User:
        """
        Finds user by kwargs.

        Queries 'users' table. Returns first match.

        Args:
            **kwargs: User attributes.

        Returns:
            User: Matching User object.

        Raises:
            NoResultFound: If no user found.
            InvalidRequestError: If invalid attribute.
        """
        return self._session.query(User).filter_by(**kwargs).one()

    def update_user(self, user_id: int, **kwargs: str) -> None:
        """
        Updates user attributes.

        Locates user by ID. Updates attributes. Commits changes.

        Args:
            user_id (int): User ID.
            **kwargs: Attributes to update.

        Returns:
            None.

        Raises:
            NoResultFound: If user not found.
            ValueError: If invalid attribute.
            InvalidRequestError: If invalid query.
        """
        user = self.find_user_by(id=user_id)

        valid_attributes = User.__table__.columns.keys()

        for key, value in kwargs.items():
            if key not in valid_attributes:
                raise ValueError(f"Invalid user attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
