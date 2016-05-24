import logging
import uuid

from sqlalchemy import Column, String

from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base, DBSession as session, LineageBase

log = logging.getLogger(__name__)


class Gym(Base, LineageBase):
    __tablename__ = 'gym'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String(100))
    city = Column(String(100))
    MAC_address = Column(String(17), unique=True)


def get_gym(id_):
    return session.query(Gym).get(id_)


def list_gyms():
    return session.query(Gym)


def get_gym_by_MAC_address(MAC_address):
    return session.query(Gym).filter(
        Gym.MAC_address == MAC_address).one_or_none()
