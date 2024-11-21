#!/usr/bin/env python3
"""DB module.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user and commits to the database.
        """
        try:
            Ad_user = User(email=email, hashed_password=hashed_password)
            self._session.add(Ad_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            Ad_user = None
        return Ad_user

    def find_user_by(self, **kwargs) -> User:
        """Finds a user by specified filters.
        """
        flds, vals = [], []
        for ke, vl in kwargs.items():
            if hasattr(User, ke):
                flds.append(getattr(User, ke))
                vals.append(vl)
            else:
                raise InvalidRequestError()
        rslt = self._session.query(User).filter(
            tuple_(*flds).in_([tuple(vals)])
        ).first()
        if rslt is None:
            raise NoResultFound()
        return rslt

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's details by user ID.
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        updt_sorc = {}
        for ke, vl in kwargs.items():
            if hasattr(User, ke):
                updt_sorc[getattr(User, ke)] = vl
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            updt_sorc,
            synchronize_session=False,
        )
        self._session.commit()
