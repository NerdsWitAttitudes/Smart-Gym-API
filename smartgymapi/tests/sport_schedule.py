import uuid
from datetime import datetime

from pyramid import testing

from smartgymapi.handlers.sport_schedule import RESTSportScheme
from smartgymapi.lib.factories.sport_schedule import SportScheduleFactory
from smartgymapi.models.user import User
from smartgymapi.tests import UnitTestCase


class UnitSportScheduleTest(UnitTestCase):
    salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
    hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS' \
                      'Qio8ECMHzXjizx4gqn1Rq'

    user = User(id=uuid.uuid4(),
                first_name='test_name',
                last_name='testing',
                password_hash=hashed_password,
                password_salt=salt,
                email='testingemail@testing.com',
                country='The Netherlands',
                date_of_birth=datetime.now())

    def setUp(self):
        super().setUp()

    def test_get_sport_schedule(self):
        self.session.add(self.user)
        self.session.flush()

        request = testing.DummyRequest()
        request.context = SportScheduleFactory

        RESTSportScheme(request).get()

        self.assertEqual(request.response.status_code, 200)

    def test_add_sport_schedule(self):
        request = testing.DummyRequest()
        request.context = SportScheduleFactory
        request.user = self.user
        request.json_body = {
            'name': 'Testing sport schedule name',
            'reminder_minutes': 15,
            'time': datetime.time(datetime.now()),
            'weekdays': [
                1,
                3,
                4
            ]
        }

        self.assertEqual(request.response.status_code, 200)
