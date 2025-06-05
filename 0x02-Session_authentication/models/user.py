#!/usr/bin/env python3
""" User module
"""
from models.base import Base
import bcrypt
import uuid


class User(Base):
    """ User class
    """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance.
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")  # This will be hashed on set
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")

    @property
    def password(self) -> str:
        """ password getter
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, pwd: str):
        """ password setter
        """
        if pwd is None or not isinstance(pwd, str):
            self._hashed_password = None
        else:
            self._salt = bcrypt.gensalt()
            self._hashed_password = bcrypt.hashpw(
                pwd.encode('utf-8'), self._salt
            )

    def is_valid_password(self, pwd: str) -> bool:
        """ Check if password is valid
        """
        if pwd is None or not isinstance(pwd, str):
            return False
        if self._hashed_password is None:
            return False
        return bcrypt.checkpw(
            pwd.encode('utf-8'), self._hashed_password
        )

    def to_json(self) -> dict:
        """ To JSON
        """
        obj_json = super().to_json()
        if '_hashed_password' in obj_json:
            del obj_json['_hashed_password']
        if '_salt' in obj_json:
            del obj_json['_salt']
        return obj_json

    @classmethod
    def search(cls, attributes: dict) -> list:
        """ Search
        """
        all_users = cls.all()
        found_users = []
        for user in all_users:
            match = True
            for key, value in attributes.items():
                if not hasattr(user, key) or getattr(user, key) != value:
                    match = False
                    break
            if match:
                found_users.append(user)
        return found_users

    @classmethod
    def get_user_from_session_id(cls, session_id: str) -> any:
        """
        Retrieve a user based on their session ID.
        """
        if session_id is None:
            return None
        users = cls.search({"session_id": session_id})
        if users:
            return users[0]
        return None
