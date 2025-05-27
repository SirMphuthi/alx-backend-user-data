#!/usr/bin/env python3
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if path == "/":
            normalized_path = "/"
        else:
            normalized_path = path.rstrip('/') + '/'

        for excluded_path_candidate in excluded_paths:
            if not isinstance(excluded_path_candidate, str) or excluded_path_candidate is None:
                continue

            if excluded_path_candidate == "/":
                normalized_excluded_path = "/"
            else:
                normalized_excluded_path = excluded_path_candidate.rstrip('/') + '/'

            if normalized_path == normalized_excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        return None
