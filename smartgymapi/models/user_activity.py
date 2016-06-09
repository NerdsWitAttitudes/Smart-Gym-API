import logging
import uuid

from sqlalchemy import (
    Column, Date, DateTime, ForeignKey, cast, func, desc)
from sqlalchemy.ext.hybrid import hybrid_property
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

    @hybrid_property
    def weekday(self):
        """Returns the weekday for the startdate ranging from 1 to 7.

        Where 1 is Monday and 7 is Sunday. The reason it ranges from 1 to 7
        is to match already existing implementations in the project.
        """

        return func.extract('dow', self.start_date) + 1

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
                UserActivity.start_date) == date.isocalendar()[2]).order_by(
        desc(UserActivity.start_date))


def get_favorite_weekdays_for_user(user):
    """ Get the user's favorite weekdays to go to the gym.

    Ordered from most favorite to least favorite.
    """

    return session.query(UserActivity.weekday)\
        .filter(UserActivity.user == user)\
        .order_by(
            func.count(UserActivity.weekday).desc())\
        .group_by(UserActivity.weekday)
