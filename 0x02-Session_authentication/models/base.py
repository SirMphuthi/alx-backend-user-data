#!/usr/bin/env python3
""" Base module
"""
from datetime import datetime
import os
import uuid
import json # <--- ADD THIS LINE

class Base:
    """ Base class
    """
    def __init__(self):
        """ Init
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_json(self) -> dict:
        """ To JSON
        """
        obj_json = {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        for key, value in self.__dict__.items():
            if key not in [
                "id", "created_at", "updated_at", "_db", "_salt", "_hashed_password"
            ]:
                obj_json[key] = value
        return obj_json

    @classmethod
    def load_from_file(cls):
        """ Load from file
        """
        file_path = f"db/{cls.__name__}.json"
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            data = json.load(f)
        return [cls(**item) for item in data]

    def save(self):
        """ Save
        """
        # from models.user import User # This import is not needed here
        obj_json = self.to_json()
        file_path = f"db/{type(self).__name__}.json"
        all_data = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try: # Add a try-except block here for empty/malformed JSON
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    all_data = [] # If file is empty or malformed, start fresh

        # Update existing or add new
        found = False
        for i, item in enumerate(all_data):
            if item.get('id') == self.id:
                all_data[i] = obj_json
                found = True
                break
        if not found:
            all_data.append(obj_json)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(all_data, f, indent=2)

    def remove(self):
        """ Remove
        """
        file_path = f"db/{type(self).__name__}.json"
        if not os.path.exists(file_path):
            return

        all_data = []
        with open(file_path, 'r') as f:
            try: # Add a try-except block here for empty/malformed JSON
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = [] # If file is empty or malformed, treat as empty

        all_data = [item for item in all_data if item.get('id') != self.id]

        with open(file_path, 'w') as f:
            json.dump(all_data, f, indent=2)


    @classmethod
    def count(cls) -> int:
        """ Count
        """
        users = cls.all()
        return len(users)


    @classmethod
    def all(cls) -> list:
        """ All
        """
        # from models.user import User # This import is not strictly needed here if User is imported at top level
        list_objs = []
        file_path = f"db/{cls.__name__}.json"
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as f:
            try: # Add a try-except block here for empty/malformed JSON
                data = json.load(f)
            except json.JSONDecodeError:
                return [] # If file is empty or malformed, return empty list

        for obj in data:
            if cls.__name__ == "User":
                # Assuming User constructor can handle dict unpacking
                # if user.py is properly set up with kwargs
                from models.user import User # Ensure User is available
                list_objs.append(User(**obj))
            else:
                # Generic case, if you add other models later
                # This needs to be able to reconstruct the object correctly
                instance = cls()
                for k, v in obj.items():
                    if k in ['created_at', 'updated_at'] and isinstance(v, str):
                        setattr(instance, k, datetime.fromisoformat(v))
                    elif k == 'id': # Ensure id is set correctly
                        instance.id = v
                    elif k == '_hashed_password': # Handle private attributes from saved data
                        instance._hashed_password = v.encode('utf-8') if isinstance(v, str) else v
                    elif k == '_salt':
                        instance._salt = v.encode('utf-8') if isinstance(v, str) else v
                    else:
                        setattr(instance, k, v)
                list_objs.append(instance)
        return list_objs

    @classmethod
    def get(cls, id) -> any:
        """ Get
        """
        for obj in cls.all():
            if obj.id == id:
                return obj
        return None
