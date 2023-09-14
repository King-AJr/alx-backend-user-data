#!/usr/bin/env python3
"""
module to handle authentication
"""
from flask import jsonify
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.exc import NoResultFound
from typing import Union
from uuid import uuid4

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
    password = password.encode("utf-8")

    # Use bcrypt's hashpw function to hash the password with a
    # randomly generated salt
    hashed_pwd = hashpw(password, gensalt())

    # Return the hashed password as bytes
    return hashed_pwd


def _generate_uuid() -> str:
    """
    return a string representation of a new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

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
        if (
            email is None
            or email == ""
            or not isinstance(email, str)
            or password is None
            or password == ""
            or not isinstance(password, str)
        ):
            raise ValueError

        try:
            # Check if a user with the same email already
            # exists in the database
            self._db.find_user_by(email=email)
        except NoResultFound:
            # If no user with the provided email is found,
            # proceed to register the new user
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        else:
            # If a user with the same email exists, raise an error
            raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials.

        Args:
            self (object): The instance of the Auth class.
            email (str): The email address entered by the user.
            password (str): The password entered by the user.

        Returns:
            bool: True if the provided credentials are valid; False otherwise.
        """
        try:
            if email == "" or password == "":
                return False

            # Attempt to find the user by email
            existing_user = self._db.find_user_by(email=email)

            if existing_user:
                # Encode the password as bytes
                password = password.encode("utf-8")
                # Compare hashed passwords
                valid_pwd = checkpw(password, existing_user.hashed_password)
                # Return True if passwords match
                return valid_pwd
        except NoResultFound:
            # Return False if no user found or password doesn't match
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """
        Create a new session for a user based on their email.

        Args:
            self (object): The instance of the class.
            email (str): The email of the user for whom the
            session is being created.

        Returns:
            str: A unique session ID if the session is successfully
                 created, or None if
                 no user with the provided email is found in the database.
        """
        try:
            # Attempt to find the user by email in the database
            user = self._db.find_user_by(email=email)

            # If a user with the email is found, create a new session
            if user:
                # Generate a unique session ID
                session_id = _generate_uuid()

                # Update the user's session ID in the database
                self._db.update_user(user.id, session_id=session_id)

                # Return the generated session ID
                return session_id
        except NoResultFound:
            # Return None if no user with the provided email is found
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)

            if user:
                return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        try:
            user = self._db.find_user_by(id=id)
            if user:
                self._db.update_user(user_id, session_id=None)
                return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid4())
            self._db.update_user(user.id, reset_token=reset_token)
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password)
            self._db.update_user(user.id, reset_token=None)
            return user.reset_token
        except NoResultFound:
            raise ValueError
