#!/usr/bin/env python3
"""
This script defines a `SessionAuth` class that inherits
from the `Auth` class in the `api.v1.auth` module.
"""

from api.v1.auth.auth import Auth  # Import the base Auth class
from uuid import uuid4  # Import the uuid4 function for generating session IDs
from models.user import User


class SessionAuth(Auth):
    """
    `SessionAuth` is a subclass of `Auth`, which handles
    session-based authentication.
    """

    user_id_by_session_id = {}  # Dictionary to store user IDs by session ID

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a new session and associates it with a user.

        Args:
            user_id (str): The user ID to associate with the session.

        Returns:
            str: The generated session ID or None if invalid input.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid4())  # Generate a unique session ID
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a session ID.

        Args:
            session_id (str): The session ID for which to retrieve the user ID.

        Returns:
            str: The user ID associated with session ID or None if not found
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Use the get method to retrieve the user ID from the dictionary
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the current user associated with a session.

        Args:
            request (Request): The Flask request object (optional).

        Returns:
            User: The User object representing the current user, or None if not found.
        """
        # Get the session cookie value from the request
        cookie = self.session_cookie(request)
        
        # Retrieve the user ID associated with the session ID
        user_id = self.user_id_for_session_id(cookie)
        
        # Get the User object using the retrieved user ID
        user = User.get(user_id)
        
        return user
