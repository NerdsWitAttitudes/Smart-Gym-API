import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy_utils import UUIDType
from smartgymapi.models.meta import Base, LineageBase, DBSession as session


class UserActivity(Base, LineageBase):
    __tablename__ = 'user_activity'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))

    @property
    def minutes(self):
        total = self.end_date - self.start_date
        return (total.seconds % 3600) // 60

    @property
    def date(self):
        return self.start_date.date()

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def get_user_activity(id_):
    return session.query(UserActivity).get(id_)


def list_user_activities(date=None):
    q = session.query(UserActivity)
    if date:
        q = q.filter(UserActivity.date == date)
    return q


def predict_user_activities(date):
    q = session.query(UserActivity)
    q = q.filter("strftime('%w', start_date) = :dow").params(dow=1)
    return q
