import logging
import uuid

from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base

log = logging.getLogger(__name__)


class Gym(Base):
    __tablename__ = 'gym'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    city = Column(String(100))
    MAC_address = Column(String(17))
