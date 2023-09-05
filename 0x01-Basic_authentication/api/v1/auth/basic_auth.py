#!/usr/bin/env python3
"""
This module contains the `BasicAuth` class, which
implements methods necessary for Basic Authentication.
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Class to implement authentication using
    the Basic Authentication algorithm.
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the base64-encoded portion of an authorization header.

        Args:
            authorization_header (str): The authorization header string.

        Returns:
            str: The base64-encoded portion of the header, or None if invalid.
        """
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        base = "Basic "
        if authorization_header.startswith(base):
            return authorization_header[len(base):]
        else:
            return None
