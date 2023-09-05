#!/usr/bin/env python3
"""
This module contains the `BasicAuth` class, which
implements methods necessary for Basic Authentication.
"""

from api.v1.auth.auth import Auth
from typing import TypeVar
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
        Decode a Base64-encoded authorization header and return
        the decoded string.

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

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Extract user credentials (username and password) from a decoded
        Base64-encoded
        authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded
            Base64-encoded authorization header.

        Returns:
            Tuple[str, str]: A tuple containing the extracted username and
            password, or None if
            the input is invalid or doesn't contain both username and password.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                        decoded_base64_authorization_header, str):
            return (None, None)

        # Check if the decoded header contains a colon (':') separator
        if decoded_base64_authorization_header.count(":") > 0:
            # Split the decoded header into username and password
            splitted_text = decoded_base64_authorization_header.split(":", 1)
            if len(splitted_text) == 2:
                return (splitted_text[0], splitted_text[1])
            else:
                # Return None if there are more than one colon separators
                return (None, None)
        else:
            # Return None if there is no colon separator in the input
            return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_password: str) -> TypeVar('User'):
        """
        Get a User object based on provided credentials.

        This method attempts to retrieve
        a User object by searching for a user with
        the given email
        and validating the provided password.

        Args:
            self (Auth): The Auth instance.
            user_email (str): The email address of the user.
            user_password (str): The user's password.

        Returns:
            TypeVar('User'): The User object if valid credentials are provided,
            or None if not found
            or invalid.
    """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_password is None or not isinstance(user_password, str):
            return None

        try:
            # Search for users with the provided email
            users = User.search({"email": user_email})

            # If no users found or the list is empty, return None
            if not users or users == []:
                return None

            # Iterate through the list of users check if the password is valid
            for user in users:
                if user.is_valid_password(user_password):
                    return user

            # If no user with valid credentials is found, return None
            return None
        except Exception:
            # Handle any exceptions and return None in case of an error
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Extract the current user from an HTTP request.

        Args:
            request (Request): The Flask request object (optional).

        Returns:
            User: The current user if authentication is successful,
            or None if not.
        """
        # Get the authorization header from the request
        authorization_header = self.authorization_header(request)

        if authorization_header is not None:
            # Extract the base64-encoded token from the authorization header
            base64_token = self.extract_base64_authorization_header(
                    authorization_header)

            if base64_token is not None:
                # Decode the base64 token to obtain user credentials
                decoded_credentials = self.decode_base64_authorization_header(
                        base64_token)

                if decoded_credentials is not None:
                    # Extract email and password from the decoded credentials
                    email, password = self.extract_user_credentials(
                            decoded_credentials)

                    if email is not None:
                        return self.user_object_from_credentials(
                                email, password)

        # If any step fails or no user is found, return None
        return None
