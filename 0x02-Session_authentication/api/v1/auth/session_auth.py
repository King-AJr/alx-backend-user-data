#!/usr/bin/env python3
"""
This script defines a SessionAuth class that inherits
from the Auth class in the api.v1.auth module.
"""

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    SessionAuth is a subclass of Auth, which handles
    session-based authentication.
    """
    pass
