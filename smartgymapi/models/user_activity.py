import logging
import uuid

from sqlalchemy import (
    Column, Date, DateTime, ForeignKey, cast, func, or_, and_)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import extract

from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base, DBSession as session, LineageBase
from smartgymapi.models.weather import Weather

log = logging.getLogger(__name__)


class UserActivity(Base, LineageBase):
    __tablename__ = 'user_activity'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    start_date = Column(DateTime(timezone=True), default=func.now())
    end_date = Column(DateTime(timezone=True))

    weather_id = Column(UUIDType, ForeignKey('weather.id'))
    user_id = Column(UUIDType, ForeignKey('user.id'))
    gym_id = Column(UUIDType, ForeignKey('gym.id'))

    weather = relationship('Weather', backref='user_activitie')
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
    return session.query(UserActivity).join(
        Weather, UserActivity.weather_id == Weather.id).filter(
        extract('dow',
                UserActivity.start_date) == date.isocalendar()[2])

    # .filter(
    #     and_(Weather.rain == weather[
    #         date_list[extract('hour', UserActivity.start_date)]]['rain'],
    #         or_(
    #             Weather.temperature >= weather[
    #                 date_list[UserActivity.start_date.hour]][
    #                 'temperature'] - 5,
    #             Weather.temperature <= weather[
    #                 date_list[UserActivity.start_date.hour]][
    #                 'temperature'] + 5
    #     )
    #     ))
