#!/usr/bin/env python3
""" Main 0
"""
import base64
from models.user import User
import os
import json # <--- ADD THIS LINE

# Clear db/User.json to ensure a fresh start for the test user
user_db_path = "db/User.json"
if os.path.exists(user_db_path):
    os.remove(user_db_path)
    print(f"Removed existing {user_db_path} for a clean test run.")

""" Create a user test """
user_email = "bob@hbtn.io"
user_clear_pwd = "H0lbertonSchool98!"

user = User()
user.email = user_email
user.password = user_clear_pwd # Setter will hash this
print("New user created with ID: {}".format(user.id))
user.save() # This will save the user with the hashed password

basic_clear = "{}:{}".format(user_email, user_clear_pwd)
print("Basic Base64 for curl: {}".format(base64.b64encode(basic_clear.encode('utf-8')).decode("utf-8")))
