import logging
import uuid

from sqlalchemy import (
    Boolean, Column, Date, DateTime, Float, ForeignKey, cast, func)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import extract

from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base, DBSession as session, LineageBase


log = logging.getLogger(__name__)


class UserActivity(Base, LineageBase):
    __tablename__ = 'user_activity'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    start_date = Column(DateTime(timezone=True), default=func.now())
    end_date = Column(DateTime(timezone=True))

    raining_outside = Column(Boolean, default=False)
    temparature = Column(Float(precision=1))

    user_id = Column(UUIDType, ForeignKey('user.id'))
    gym_id = Column(UUIDType, ForeignKey('gym.id'))

    user = relationship('User', backref='user_activities')
    gym = relationship('Gym')

    @property
    def minutes(self):
        total = self.end_date - self.start_date
        return (total.seconds % 3600) // 60

    @property
    def date(self):
        return self.start_date.date()

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def get_user_activity(id_):
    return session.query(UserActivity).get(id_)


def list_user_activities(date=None):
    q = session.query(UserActivity)
    if date:
        q = q.filter(cast(UserActivity.start_date, Date) == date)
    return q


def list_user_activities_for_prediction(date):
    return session.query(UserActivity).filter(
        extract('dow', UserActivity.start_date) == date.isocalendar()[2])
