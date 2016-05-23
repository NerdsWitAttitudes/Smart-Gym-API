import logging
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from smartgymapi.models.meta import Base

log = logging.getLogger(__name__)


class UserActivity(Base):
    __tablename__ = 'user_activity'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    start_date = Column(DateTime(timezone=True), default=func.now())
    end_date = Column(DateTime(timezone=True))

    user_id = Column(UUIDType, ForeignKey('user.id'))
    gym_id = Column(UUIDType, ForeignKey('gym.id'))

    user = relationship('User')
    gym = relationship('Gym')

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)
