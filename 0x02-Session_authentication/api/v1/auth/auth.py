#!/usr/bin/env python3
"""
This module manages API authentication.
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """
    This class manages API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path.

        Args:
            path (str): The path to check for authentication.
            excluded_paths (List[str]): A list of paths that
            are exempt from authentication.

        Returns:
            bool: True if authentication is required, False if not.
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        split_path = path.split('/')
        for ex_path in excluded_paths:
            ex_paths = ex_path.split('/')
            if len(split_path) > 3 and len(ex_paths) > 3\
                    and split_path[3] == ex_paths[3]:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from a Flask request object.

        Args:
            request (Request): The Flask request object (optional).

        Returns:
            str: The authorization header.
        """
        if request is not None:
            headers = request.headers
            if 'Authorization' in headers:
                return headers['Authorization']
            else:
                return None

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user.

        Args:
            request (Request): The Flask request object (optional).

        Returns:
            User: The current user.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie value from a Flask request object.

        Args:
            request (Request): The Flask request object (optional).

        Returns:
            str: The value of the session cookie, or None if not found.
        """
        if request is None:
            return None

        # Get the name of the session cookie from environment variables
        cookie_name = getenv("SESSION_NAME")

        # Retrieve the value of the session cookie from the request's cookies
        cookie_value = request.cookies.get(cookie_name)

        return cookie_value
