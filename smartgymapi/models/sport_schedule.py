import uuid

from sqlalchemy import (Column, String, Integer, ForeignKey,
                        UniqueConstraint, Time, Boolean, func)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base, DBSession, LineageBase


class SportSchedule(Base, LineageBase):
    __tablename__ = 'sport_schedule'
    __table_args__ = (UniqueConstraint('user_id', 'name',
                                       name='sport_schedule_name_uc'),)

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType, ForeignKey('user.id'))
    name = Column(String(100))
    reminder_minutes = Column(Integer)
    time = Column(Time(timezone=True))
    weekdays = Column(Integer)
    is_active = Column(Boolean)

    user = relationship('User')

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def list_sport_schedules(user):
    return DBSession.query(SportSchedule).filter(SportSchedule.user == user)


def get_sport_schedule(id_):
    return DBSession.query(SportSchedule).get(id_)


def get_favorite_weekdays_for_user(user):
    """ Get the user's favorite weekdays to go to the gym.

    Ordered from most favorite to least favorite.
    """

    return DBSession.query(SportSchedule.weekdays)\
        .filter(SportSchedule.user == user)\
        .order_by(
            func.count(SportSchedule.weekdays).desc())
