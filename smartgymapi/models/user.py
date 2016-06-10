import datetime
import logging
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, func, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base, LineageBase, DBSession as session

log = logging.getLogger(__name__)


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

    self_to_buddies = relationship(
        "User",
        primaryjoin="Buddy.user_1_id==User.id",
        secondaryjoin="Buddy.user_2_id==User.id",
        secondary="buddy",
        backref="buddies_to_self")
    sport_schedules = relationship("SportSchedule", uselist=True)

    @hybrid_property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def buddies(self):
        return self.self_to_buddies + self.buddies_to_self

    @property
    def buddy_ids(self):
        return [user.id for user in self.buddies]

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


class Buddy(Base):
    __tablename__ = 'buddy'

    user_1_id = Column(UUIDType(binary=False), ForeignKey('user.id'),
                       primary_key=True)
    user_2_id = Column(UUIDType(binary=False), ForeignKey('user.id'),
                       primary_key=True)
    buddies_since = Column(DateTime, default=datetime.datetime.utcnow)


def list_users(country=None, exclude=None, term='', offset=0, limit=10):
    q = session.query(User).filter(
        term in User.full_name)

    if country:
        q = q.filter(User.country == country)

    if exclude:
        q = q.filter(~User.id.in_(exclude))

    return q.offset(offset).limit(limit)


def get_user(id_):
    return session.query(User).get(id_)


def get_user_by_email(email):
    return session.query(User).filter(User.email == email).one()
