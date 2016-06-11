import datetime
import uuid

from pyramid import testing
from pyramid.httpexceptions import HTTPCreated

from smartgymapi.handlers.cardio_activity import RESTCardioActivty
from smartgymapi.lib.factories.cardio_activity import \
    CardioActivityFactory
from smartgymapi.models.user import User
from smartgymapi.tests import UnitTestCase


class UnitCardioActivityTest(UnitTestCase):
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
                date_of_birth=datetime.datetime.now())

    def setUp(self):
        super().setUp()

    def test_get_cardio_activity(self):
        self.session.add(self.user)
        self.session.flush()

        request = testing.DummyRequest()
        request.context = CardioActivityFactory

        RESTCardioActivty(request).get()

        self.assertEqual(request.response.status_code, 200)

    def test_start_cardio_activity(self):
        activity_id = 'a920093a-7fa5-440a-a257-93add88cf8f9'

        request = testing.DummyRequest()
        request.context = CardioActivityFactory
        request.json_body = {'activity_id': activity_id}

        try:
            RESTCardioActivty(request).post()
        except HTTPCreated:
            self.assertEqual(request.response.status_code, 200)
