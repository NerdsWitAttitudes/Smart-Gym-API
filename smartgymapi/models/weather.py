import logging
import uuid

from sqlalchemy import (
    Boolean, Column, DateTime, Float, func)

from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base, DBSession as session


log = logging.getLogger(__name__)


class Weather(Base):
    __tablename__ = 'Weather'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime(timezone=True), default=func.now())

    raining_outside = Column(Boolean, default=False)
    temparature = Column(Float(precision=1))

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def get_weather(id_):
    return session.query(Weather).get(id_)
