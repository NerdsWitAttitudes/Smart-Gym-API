import uuid

from sqlalchemy import Column, String, ForeignKey, relationship, DateTime, func
from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base, LineageBase, DBSession as session


class Device(Base, LineageBase):
    __tablename__ = 'device'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    device_address = Column(String(100))
    device_class = Column(String(100))
    client_address = Column(String(100))
    user_id = Column(UUIDType, ForeignKey('user.id'))
    last_used = Column(DateTime(timezone=True), default=func.now())

    user = relationship("User")

    def set_field(self, data):
        for key, value in data.items():
            setattr(self, key, value)


def get_device_by_device_address(device_address):
    return session.query(Device).filter(
        Device.device_address == device_address).one()
