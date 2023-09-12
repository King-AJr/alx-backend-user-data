#!/usr/bin/env python3
"""
module to handle authentication
"""
from bcrypt import hashpw, gensalt

import bcrypt


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
    hashed_pwd = bcrypt.hashpw(password, bcrypt.gensalt())

    # Return the hashed password as bytes
    return hashed_pwd
