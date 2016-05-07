import logging
import uuid

from smartgymapi.models.meta import Base, DBSession as session, LineageBase

from sqlalchemy import Column, Date, DateTime, ForeignKey, cast

from sqlalchemy.orm import relationship
from sqlalchemy.sql import extract

from sqlalchemy_utils import UUIDType

log = logging.getLogger(__name__)


class UserActivity(Base, LineageBase):
    __tablename__ = 'user_activity'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))

    user_id = Column(UUIDType, ForeignKey('user.id'))

    user = relationship('User', backref='user_activities')

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
        q = q.filter(cast(UserActivity.start_date, Date) == date).all()
    return q


def predict_user_activities(date):
    q = session.query(UserActivity)
    q = q.filter(
        extract('dow', UserActivity.start_date) == date.isocalendar()[2])
    return q
