import uuid

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy_utils import UUIDType

from smartgymapi import Base, DBSession


class SportScheme(Base):
    __tablename__ = 'sport_scheme'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType, ForeignKey('user.id'))
    name = Column(String(100))
    reminder_minutes = Column(Integer)


def list_sport_schemes():
    return DBSession.query(SportScheme)
