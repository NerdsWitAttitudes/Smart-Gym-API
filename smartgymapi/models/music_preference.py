import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from smartgymapi.models.meta import Base, DBSession as session


class MusicPreference(Base):
    __tablename__ = 'music_preference'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    genre = Column(String(100))
    artist = Column(String(100))
    song_name = Column(String(100))
    spotify_uri = Column(String(100))
    spotify_category_id = Column(String(100))
    spotify_id = Column(String(100))

    user_id = Column(UUIDType, ForeignKey('user.id'))

    user = relationship("User")


def list_music_preferences():
    return session.query(MusicPreference)
