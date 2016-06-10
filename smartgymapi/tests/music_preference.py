import datetime

from pyramid import testing

from smartgymapi.tests import UnitTestCase


class MusicPreferenceTest(UnitTestCase):

    def setUp(self):
        super().setUp()

    def test_get_music_preference_succesful(self):
        from smartgymapi.models.music_preference import MusicPreference
        from smartgymapi.models.user import User
        from smartgymapi.handlers.music_preference import RESTMusicPreference

        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        user = User(id='af425ccf-3eef-4f19-9e8d-8cb86867824e',
                    first_name='test',
                    last_name='person',
                    password_hash=hashed_password,
                    password_salt=salt,
                    email='test@test.com',
                    country='The Netherlands',
                    date_of_birth=datetime.datetime.now())
        self.session.add(user)

        music_preference = MusicPreference(
            user_id=user.id,
            city='Rotterdam',
            MAC_address='24:FD:52:E6:0F:FB',
            spotify_playlist_id='2YO7LggvPHcfFC48Iq29zk')

        self.session.add(music_preference)
        self.session.flush()

        request = testing.DummyRequest()
        request.context = music_preference

        RESTMusicPreference(request).get()
        self.assertEqual(request.response.status_code, 200)
