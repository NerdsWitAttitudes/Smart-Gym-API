import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from smartgymapi.models.user_activity import UserActivity
from smartgymapi.models.meta import Base, LineageBase, DBSession


class CardioActivity(Base, LineageBase):
    __tablename__ = 'cardio_activity'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUIDType, ForeignKey('user_activity.id'),
                         nullable=False)

    start_date = Column(DateTime(timezone=True), default=datetime.now)
    end_date = Column(DateTime(timezone=True), default=None)

    cardio_type = Column(String)

    distance = Column(Integer)
    speed = Column(Float)
    calories = Column(Float)

    user_activity = relationship('UserActivity', backref='cardio_activities')

    @property
    def is_active(self):
        return self.end_date is None

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def get_cardio_activity(id_):
    return DBSession.query(CardioActivity).get(id_)


def list_cardio_activities(user_):
    return DBSession.query(CardioActivity).join(
        UserActivity, CardioActivity.activity_id == UserActivity.id
    ).filter(UserActivity.user == user_)


def is_cardio_activity_active(activity_id):
    return DBSession.query(CardioActivity).filter(
        CardioActivity.activity_id == activity_id).filter(
        CardioActivity.end_date == None).one_or_none()
