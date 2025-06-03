#!/usr/bin/env python3
"""
Integration tests for the user authentication service Flask app.

This module defines functions to test various API endpoints
like user registration, login, profile retrieval, and password reset.
It uses the 'requests' library to interact with the Flask server
and 'assert' statements to validate responses.
"""

import requests
import json
import os
import sys

# Base URL for the Flask application
BASE_URL = "http://localhost:5000"

# Global variables for test data as provided in the task
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """
    Tests the POST /users endpoint for user registration.

    Asserts for a 200 OK status code and the expected JSON payload
    for successful registration, or a 400 BAD REQUEST for
    already registered email.
    """
    print(f"--- Testing register_user({email}, {password}) ---")
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/users", data=data)

    if response.status_code == 200:
        expected_json = {"email": email, "message": "user created"}
        assert response.json() == expected_json, \
            f"register_user: Expected {expected_json}, got {response.json()}"
        print("register_user: User created successfully.")
    elif response.status_code == 400:
        expected_json = {"message": "email already registered"}
        assert response.json() == expected_json, \
            f"register_user: Expected {expected_json}, got {response.json()}"
        print("register_user: User already registered (as expected).")
    else:
        assert False, \
            f"register_user: Unexpected status {response.status_code}: " \
            f"{response.text}"
    print("register_user PASSED\n")


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Tests the POST /sessions endpoint with incorrect password.

    Asserts for a 401 UNAUTHORIZED status code.
    """
    print(f"--- Testing log_in_wrong_password({email}, {password}) ---")
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=data)
    assert response.status_code == 401, \
        f"log_in_wrong_password: Expected 401, got {response.status_code}: " \
        f"{response.text}"
    print("log_in_wrong_password: Correctly denied login with wrong password.")
    print("log_in_wrong_password PASSED\n")


def log_in(email: str, password: str) -> str:
    """
    Tests the POST /sessions endpoint for successful login.

    Asserts for a 200 OK status code and the expected JSON payload.
    Returns the session ID extracted from the 'Set-Cookie' header.
    """
    print(f"--- Testing log_in({email}, {password}) ---")
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", data=data)
    assert response.status_code == 200, \
        f"log_in: Expected 200, got {response.status_code}: {response.text}"
    expected_json = {"email": email, "message": "logged in"}
    assert response.json() == expected_json, \
        f"log_in: Expected {expected_json}, got {response.json()}"

    session_id = response.cookies.get("session_id")
    assert session_id is not None, "log_in: session_id cookie not found"
    print(f"log_in: Successfully logged in. Session ID: {session_id}")
    print("log_in PASSED\n")
    return session_id


def profile_unlogged() -> None:
    """
    Tests the GET /profile endpoint without a session ID cookie.

    Asserts for a 403 FORBIDDEN status code.
    """
    print("--- Testing profile_unlogged() ---")
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, \
        f"profile_unlogged: Expected 403, got {response.status_code}: " \
        f"{response.text}"
    print("profile_unlogged: Correctly denied access without session.")
    print("profile_unlogged PASSED\n")


def profile_logged(session_id: str) -> None:
    """
    Tests the GET /profile endpoint with a valid session ID cookie.

    Asserts for a 200 OK status code and the expected JSON payload.
    """
    print(f"--- Testing profile_logged({session_id}) ---")
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, \
        f"profile_logged: Expected 200, got {response.status_code}: " \
        f"{response.text}"
    expected_json = {"email": EMAIL}  # Using global EMAIL for validation
    assert response.json() == expected_json, \
        f"profile_logged: Expected {expected_json}, got {response.json()}"
    print("profile_logged: Successfully retrieved profile.")
    print("profile_logged PASSED\n")


def log_out(session_id: str) -> None:
    """
    Tests the DELETE /sessions endpoint for user logout.

    Asserts for a 302 FOUND status code (redirection) and
    that the redirection leads to the expected GET / response.
    """
    print(f"--- Testing log_out({session_id}) ---")
    cookies = {"session_id": session_id}
    # Allow redirects to check the final status code after redirect
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies,
                               allow_redirects=True)
    # After redirect, the final response should be from GET /
    assert response.status_code == 200, \
        f"log_out: Expected 200 (after redirect), got {response.status_code}:"\
        f" {response.text}"
    expected_json = {"message": "Bienvenue"}
    assert response.json() == expected_json, \
        f"log_out: Expected {expected_json} after redirect, " \
        f"got {response.json()}"
    print("log_out: Successfully logged out and redirected.")
    print("log_out PASSED\n")


def reset_password_token(email: str) -> str:
    """
    Tests the POST /reset_password endpoint for token generation.

    Asserts for a 200 OK status code and the expected JSON payload.
    Returns the generated reset token.
    """
    print(f"--- Testing reset_password_token({email}) ---")
    data = {"email": email}
    response = requests.post(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200, \
        f"reset_password_token: Expected 200, got {response.status_code}: " \
        f"{response.text}"
    response_json = response.json()
    assert response_json.get("email") == email, \
        f"reset_password_token: Email mismatch. Expected {email}, " \
        f"got {response_json.get('email')}"
    reset_token = response_json.get("reset_token")
    assert reset_token is not None, \
        "reset_password_token: reset_token not found in response"
    print(f"reset_password_token: Generated token: {reset_token}")
    print("reset_password_token PASSED\n")
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Tests the PUT /reset_password endpoint for password update.

    Asserts for a 200 OK status code and the expected JSON payload.
    """
    print(f"--- Testing update_password({email}, {reset_token}, "
          f"{new_password}) ---")
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(f"{BASE_URL}/reset_password", data=data)
    assert response.status_code == 200, \
        f"update_password: Expected 200, got {response.status_code}: " \
        f"{response.text}"
    expected_json = {"email": email, "message": "Password updated"}
    assert response.json() == expected_json, \
        f"update_password: Expected {expected_json}, got {response.json()}"
    print("update_password: Password updated successfully.")
    print("update_password PASSED\n")


# --- Main execution block ---
# Global variables as provided in the task description
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    # Ensure 'requests' is installed: pip3 install requests
    # Ensure your Flask app (app.py) is running in a separate terminal:
    # python3 app.py

    print("--- Starting API Integration Tests ---")

    try:
        # Test sequence as per task description
        register_user(EMAIL, PASSWD)
        log_in_wrong_password(EMAIL, NEW_PASSWD)
        profile_unlogged()
        session_id = log_in(EMAIL, PASSWD)
        profile_logged(session_id)
        log_out(session_id)
        reset_token = reset_password_token(EMAIL)
        update_password(EMAIL, reset_token, NEW_PASSWD)
        # After password update, log in with the NEW password
        log_in(EMAIL, NEW_PASSWD)

        print("--- All API Integration Tests Passed Successfully! ---")
    except AssertionError as e:
        print(f"\n!!! TEST FAILED: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"\n!!! CONNECTION ERROR: Ensure your Flask app is running "
              f"at {BASE_URL} in a separate terminal. Details: {e}",
              file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n!!! AN UNEXPECTED ERROR OCCURRED: {e}", file=sys.stderr)
        sys.exit(1)
