import datetime
import uuid

from pyramid import testing

from smartgymapi.tests import UnitTestCase


class UnitMusicPreferenceTest(UnitTestCase):

    def setUp(self):
        super().setUp()

    def test_get_music_preference_succesful(self):
        from smartgymapi.models.music_preference import MusicPreference
        from smartgymapi.models.user import User
        from smartgymapi.handlers.music_preference import RESTMusicPreference

        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'
        user_id = uuid.uuid4()
        user = User(id=user_id,
                    first_name='test',
                    last_name='person',
                    password_hash=hashed_password,
                    password_salt=salt,
                    email='test@test.com',
                    country='The Netherlands',
                    date_of_birth=datetime.datetime.now())
        self.session.add(user)

        music_preference = MusicPreference(
            id=uuid.uuid4(),
            user_id=user_id,
            genre='dance')

        self.session.add(music_preference)
        self.session.flush()

        request = testing.DummyRequest()
        request.context = music_preference

        RESTMusicPreference(request).get()
        self.assertEqual(request.response.status_code, 200)
