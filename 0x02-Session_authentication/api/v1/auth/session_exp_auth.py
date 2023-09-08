#!/usr/bin/env python3
"""
implement expiration of sessions
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class inherits from SessionAuth and
    adds session expiration functionality.
    """

    def __init__(self):
        """
        Initializes the SessionExpAuth instance.

        Assigns the session_duration attribute based on the
        SESSION_DURATION environment variable, cast to an integer.
        If the environment variable doesn't exist or can't be parsed,
        assigns 0 as the default session_duration.
        """
        super().__init__()  # Call the parent class's constructor

        # Get the session duration from the environment variable
        session_duration_str = getenv("SESSION_DURATION")

        try:
            self.session_duration = int(session_duration_str)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a new session and associates it with a user.

        Args:
            user_id (str): The user ID to associate with the session.

        Returns:
            str: The generated session ID or None if creation fails.
        """
        # Call the parent class's create_session method
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        # Create a session dictionary
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        # Store the session dictionary using the session ID as the key
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID associated with a session ID.

        Args:
            session_id (str): The session ID for which to retrieve the user ID.

        Returns:
            str: The user ID associated with the session ID
            or None if not found.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")

        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > expiration_time:
            return None

        return session_dict.get("user_id")
