#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User, Base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email address of the new user.
            hashed_password (str): The hashed password of the new user.

        Returns:
            User: The newly created User object.
        """
        # Create a new User object with the provided email and hashed_password
        new_user = User(email=email, hashed_password=hashed_password)

        # Add the new_user object to the session (pending database insertion)
        self._session.add(new_user)

        # Commit the transaction to persist the new user to the database
        self._session.commit()

        # Return the newly created User object
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided keyword arguments.

        Args:
            **kwargs: Keyword arguments representing search criteria.

        Returns:
            User: The found user.

        Raises:
            InvalidRequestError: If no search criteria are provided.
            NoResultFound: If no user is found matching the criteria.
        """
        # Check if no keyword arguments were provided
        if not kwargs:
            raise InvalidRequestError

        # Query the database using the provided keyword arguments
        user = self._session.query(User).filter_by(**kwargs).first()

        # Check if no user was found
        if user is None:
            raise NoResultFound

        # Return the found user
        return user

    def update_user(self, id: int, **kwargs) -> None:
        """
        Update user information in the database based on the
        provided user ID and keyword arguments.

        Args:
            id (int): The ID of the user to be updated.
            **kwargs: Keyword arguments representing fields
            and their new values to update.

        Raises:
            ValueError: If a provided field (key) in kwargs
            does not exist in the user object.

        Returns:
            None: This function does not return a value
            explicitly but updates the user information in the database.
        """
        if id:
            # Find the user in the database by ID
            user = self.find_user_by(id=id)

            # Iterate through keyword arguments (kwargs)
            for k, v in kwargs.items():
                # Check if the user object has an attribute
                # matching the provided field (k)
                if not hasattr(user, k):
                    raise ValueError

                # Update the user's attribute with the new value (v)
                setattr(user, k, v)

            # Commit the changes to the database
            self._session.commit()
