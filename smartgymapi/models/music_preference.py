import logging
import uuid

from sqlalchemy import (
    Column, ForeignKey, String)
from sqlalchemy.orm import relationship

from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base, DBSession as session, LineageBase

log = logging.getLogger(__name__)


class MusicPreference(Base, LineageBase):
    __tablename__ = 'music_preference'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    artist = Column(String(100))
    user_id = Column(UUIDType, ForeignKey('user.id'))

    user = relationship('User', backref='music_preferences')

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def get_music_preference(id_):
    return session.query(MusicPreference).get(id_)


def list_music_preferences(user_ids=[]):
    q = session.query(MusicPreference)
    return q
