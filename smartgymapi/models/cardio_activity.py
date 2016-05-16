import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, DateTime, Float
from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base, LineageBase, DBSession


class CardioActivity(Base, LineageBase):
    __tablename__ = 'cardio_activity'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    activity_id = Column(UUIDType, ForeignKey('user_activity.id'), nullable=False)

    start_date = Column(DateTime(timezone=True), default=datetime.now)
    end_date = Column(DateTime(timezone=True), onupdate=datetime.now)

    distance = Column(Integer, default=333)
    speed = Column(Float)
    calories = Column(Float)

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def get_cardio_activity(id_):
    return DBSession.query(CardioActivity).get(id_)


def list_cardio_activities():
    return DBSession.query(CardioActivity)
