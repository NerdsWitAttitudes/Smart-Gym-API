import datetime
import uuid

from pyramid import testing

from smartgymapi.tests import UnitTestCase, FunctionalTestCase


class FunctionalUserActivityTest(FunctionalTestCase):

    def test_get_user_activity_succesful(self):
        from smartgymapi.models.user import User
        from smartgymapi.models.user_activity import UserActivity
        from smartgymapi.models.weather import Weather
        from smartgymapi.models.gym import Gym

        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        gym_id = uuid.uuid4()
        gym = Gym(
            id=gym_id,
            name='test',
            city='Rotterdam',
            MAC_address='24:FD:52:E6:0F:FB',
            spotify_playlist_id='2YO7LggvPHcfFC48Iq29zk')
        self.session.add(gym)

        user_id = uuid.uuid4()
        user = User(id=user_id,
                    first_name='test',
                    last_name='person',
                    password_hash=hashed_password,
                    password_salt=salt,
                    email='test@test.com',
                    country='The Netherlands',
                    date_of_birth=datetime.datetime.now(),
                    gym_id=gym_id)
        self.session.add(user)

        weather_id = uuid.uuid4()
        weather = Weather(
            id=uuid.uuid4(),
            temperature=15,
            rain=True)

        self.session.add(weather)

        user_activity = UserActivity(
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            weather_id=weather_id,
            user_id=user_id,
            gym_id=gym_id)
        self.session.add(user_activity)
        self.session.flush()

        response = self.app.get(
            '/user_activity')

        self.assertEqual(response.status_code, 200)


class UnitUserActivityTest(UnitTestCase):

    def setUp(self):
        super().setUp()

    def test_list_user_activity_succesful(self):
        from smartgymapi.models.user import User
        from smartgymapi.models.user_activity import UserActivity
        from smartgymapi.models.weather import Weather
        from smartgymapi.models.gym import Gym
        from smartgymapi.handlers.user_activity import RESTUserActivity
        from smartgymapi.lib.factories.user_activity import UserActivityFactory

        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        gym_id = uuid.uuid4()
        gym = Gym(
            id=gym_id,
            name='test',
            city='Rotterdam',
            MAC_address='24:FD:52:E6:0F:FB',
            spotify_playlist_id='2YO7LggvPHcfFC48Iq29zk')
        self.session.add(gym)

        user_id = uuid.uuid4()
        user = User(id=user_id,
                    first_name='test',
                    last_name='person',
                    password_hash=hashed_password,
                    password_salt=salt,
                    email='test@test.com',
                    country='The Netherlands',
                    date_of_birth=datetime.datetime.now(),
                    gym_id=gym_id)
        self.session.add(user)

        weather_id = uuid.uuid4()
        weather = Weather(
            id=uuid.uuid4(),
            temperature=15,
            rain=True)

        self.session.add(weather)

        user_activity = UserActivity(
            start_date=datetime.datetime.now(),
            end_date=datetime.datetime.now(),
            weather_id=weather_id,
            user_id=user_id,
            gym_id=gym_id)
        self.session.add(user_activity)
        self.session.flush()

        request = testing.DummyRequest()
        request.context = UserActivityFactory(None, 'UserActivity')
        RESTUserActivity(request).list()
        self.assertEqual(request.response.status_code, 200)
