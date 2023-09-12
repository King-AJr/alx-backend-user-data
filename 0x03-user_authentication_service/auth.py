#!/usr/bin/env python3
"""
module to handle authentication
"""
from bcrypt import hashpw, gensalt
from sqlalchemy.exc import NoResultFound
from typing import Union

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hashes a given plaintext password using the bcrypt hashing algorithm.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        bytes: The hashed password as bytes.
    """
    # Encode the password string as bytes using UTF-8 encoding
    password = password.encode('utf-8')

    # Use bcrypt's hashpw function to hash the password with a
    # randomly generated salt
    hashed_pwd = hashpw(password, gensalt())

    # Return the hashed password as bytes
    return hashed_pwd


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """
        Registers a new user with the given email and password.

        Args:
            email (str): The email address of the user.
            password (str): The plain-text password of the user.

        Returns:
            User: The newly registered user object.

        Raises:
            ValueError: If a user with the same email already
            exists in the database.

        Note:
            This function checks if a user with the provided email
            already exists in the database.
            If not, it hashes the provided password,
            creates a new user record, and returns it.

        """
        if email is None or email == "" or not isinstance(email, str) or\
           password is None or password == "" or not\
           isinstance(password, str):
            raise ValueError

        try:
            # Check if a user with the same email already
            # exists in the database
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                # If a user with the same email exists, raise an error
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            # If no user with the provided email is found,
            # proceed to register the new user
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user