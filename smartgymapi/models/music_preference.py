import uuid
from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType
from smartgymapi.models.meta import Base, DBSession as session


class MusicPreference(Base):
    __tablename__ = 'music_preference'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    genre = Column(String(100))
    artist = Column(String(100))
    song_name = Column(String(100))


def list_music_preferences():
    return session.query(MusicPreference)
