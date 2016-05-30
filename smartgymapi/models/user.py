import uuid
from sqlalchemy import (Column, String, DateTime, func, Boolean)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from smartgymapi.models.user_activity import UserActivity
from smartgymapi.models.meta import Base, LineageBase, DBSession as session


class User(Base, LineageBase):
    __tablename__ = 'user'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100))
    last_name = Column(String(100))
    infix = Column(String(100))
    password_hash = Column(String(100))
    password_salt = Column(String(100))
    date_created = Column(DateTime(timezone=True), default=func.now())
    date_updated = Column(DateTime(timezone=True), default=func.now(),
                          onupdate=func.current_timestamp())
    verified = Column(Boolean)
    email = Column(String(500))
    country = Column(String(200))
    date_of_birth = Column(DateTime(timezone=True))
    last_login = Column(DateTime(timezone=True))

    active_activity = relationship(
        "UserActivity",
        primaryjoin="and_(foreign(UserActivity.user_id)==User.id,"
                    "UserActivity.end_date==None)",
        uselist=False)

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def list_users():
    return session.query(User)


def get_user(id_):
    return session.query(User).get(id_)


def list_current_users_in_gym(gym_id):
    return session.query(User).join(
        UserActivity, User.id == UserActivity.id).filter(
    ).filter(UserActivity.end_date == None,
             UserActivity.gym_id == gym_id)


def get_user_by_email(email):
    return session.query(User).filter(User.email == email).one()
