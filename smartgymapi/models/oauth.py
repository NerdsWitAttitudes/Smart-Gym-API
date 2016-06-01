import datetime
import logging
import uuid

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy_utils import UUIDType

from smartgymapi.lib.encrypt import get_secure_token
from smartgymapi.models.meta import Base

log = logging.getLogger(__name__)


class OAuthClient(Base):
    __tablename__ = 'oauth_consumer'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUIDType(binary=False), default=uuid.uuid4)
    client_secret = Column(String(64), default=get_secure_token)


class OAuthAccessToken(Base):
    __tablename__ = 'oauth_access_token'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    client_id = (Column(UUIDType(binary=False),
                        ForeignKey('oauth_consumer.id')))
    access_token = Column(String(64), default=get_secure_token)
    token_type = Column(Enum("bearer"), default="bearer")
    expiry_date = Column(DateTime(timezone=True))

    @property
    def expires_in(self):
        seconds_left = (self.expiry_date - datetime.datetime.now()
                        ).total_seconds()
        return seconds_left if seconds_left > 0 else 0
