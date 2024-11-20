#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """Add a new user to the database

        Args:
            email (str): User's email address
            hashed_password (str): Hashed password for the user

        Returns:
            User: The newly created User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the User table.

        Returns:
            User: The first user matching the criteria.

        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If invalid query arguments are provided.
        """
        if not kwargs:
            raise InvalidRequestError("No filter arguments provided")

        try:
            query = self._session.query(User).filter_by(**kwargs).first()
            if not query:
                raise NoResultFound("No user found with provided criteria")
            return query
        except AttributeError:
            raise InvalidRequestError("Invalid query arguments")
