#!/usr/bin/env python3
"""
This script defines a `SessionAuth` class that inherits
from the `Auth` class in the `api.v1.auth` module.
"""

from api.v1.auth.auth import Auth  # Import the base Auth class
from uuid import uuid4  # Import the uuid4 function for generating session IDs

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
        self.user_id_by_session_id[session_id] = user_id  # Associate the session with the user
        return session_id

