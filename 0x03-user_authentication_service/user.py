#!/usr/bin/env python3
"""
module for the user model of the database
"""

# Import SQLAlchemy modules
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Create a base class for declarative models
Base = declarative_base()


# Define the User class as a SQLAlchemy model
class User(Base):
    """
    This module defines the User class,
    which represents a user in the database.

    Attributes:
        id (int): Primary key for the user.
        email (str): User's email address (not nullable).
        hashed_password (str): Hashed user password (not nullable).
        session_id (str): Session ID for user's session (nullable).
        reset_token (str): Token for resetting the user's password (nullable).
    """

    # Define the name of the database table
    __tablename__ = "users"

    # Define table columns and their data types
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
