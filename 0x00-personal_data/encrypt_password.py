#!/usr/bin/env python3
"""
module that deals with
encrypting passwords using
bcrypt
"""

import bcrypt

def hash_password(password: str) -> bytes:
    """
    expects one string argument name password
    and returns a salted, hashed password,
    which is a byte string.
    """

    encrypt = password.encode()
    hashed_pwd = bcrypt.hashpw(encrypt, bcrypt.gensalt(15))
    return hashed_pwd