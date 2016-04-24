import uuid
from sqlalchemy import Column, DateTime, Float
from sqlalchemy_utils import UUIDType
from smartgymapi.models.meta import Base, LineageBase, DBSession as session


class UserActivity(Base, LineageBase):
    __tablename__ = 'user_activity'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))

    @property
    def hours(self):
        total_time = self.end_date - self.start_date
        return total_time

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def list_user_activities():
    return session.query(UserActivity)


def get_user_activity(id_):
    return session.query(UserActivity).get(id_)
