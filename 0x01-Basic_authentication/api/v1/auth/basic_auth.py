#!/usr/bin/env python3
"""
This module contains the `BasicAuth` class, which
implements methods necessary for Basic Authentication.
"""

from api.v1.auth.auth import Auth
import base64


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


def decode_base64_authorization_header(self,
                                       base64_authorization_header:
                                       str) -> str:
    """
    Decode a Base64-encoded authorization header and return the decoded string.

    Args:
        base64_authorization_header (str): The Base64-encoded authorization
        header string.

    Returns:
        str: The decoded string if successful, or None if it's not a valid
        Base64 string.
    """
    if base64_authorization_header is None or not isinstance(
                    base64_authorization_header, str):
        return None

    try:
        # Attempt to decode the input string as Base64
        decoded_data = base64.b64decode(base64_authorization_header)

        # If decoding is successful, it's a valid Base64 string
        return decoded_data.decode('utf-8')
    except base64.binascii.Error:
        # If an error is raised, it's not a valid Base64 string
        return None
