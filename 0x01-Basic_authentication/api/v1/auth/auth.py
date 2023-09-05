#!/usr/bin/env python3
"""
module to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """
    class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        class to manage the API authentication.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        get authorization header from request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        """
        return None
