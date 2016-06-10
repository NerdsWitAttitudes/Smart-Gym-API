import datetime

from smartgymapi.lib.encrypt import hash_password, check_password
from smartgymapi.tests import TestCase, UnitTestCase, FunctionalTestCase


class EncryptTest(TestCase):
    def setUp(self):
        self.test_password = 'test123'

    def test_hash_password(self):
        hashed_password, salt = hash_password(self.test_password)
        self.assertIsNotNone(hashed_password)
        self.assertIsNotNone(salt)

    def test_check_password(self):
        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        self.assertTrue(check_password('test123', hashed_password, salt))
        self.assertFalse(check_password('notrightpass', hashed_password,
                                        salt))


class TestAuthHandlers(UnitTestCase):
    def test_login_succesful(self):
        from smartgymapi.models.user import User
        from smartgymapi.handlers.auth import login
        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        user = User(first_name='test',
                    last_name='person',
                    password_hash=hashed_password,
                    password_salt=salt,
                    email='test@test.com',
                    country='The Netherlands',
                    date_of_birth=datetime.datetime.now())
        self.session.add(user)
        self.session.flush()

        request = self.get_post_request(post={
            'email': 'test@test.com',
            'password': 'test123'
        })

        login(request)
        self.assertEqual(request.response.status_code, 200)


class FunctionalTestAuthHandlers(FunctionalTestCase):
    def test_login_succesful(self):
        from smartgymapi.models.user import User
        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        user = User(first_name='test',
                    last_name='person',
                    password_hash=hashed_password,
                    password_salt=salt,
                    email='test@test.com',
                    country='The Netherlands',
                    date_of_birth=datetime.datetime.now())
        self.session.add(user)
        self.session.flush()

        response = self.app.post_json(
            '/auth/login',
            {'email': 'test@test.com',
             'password': 'test123'})

        self.assertEqual(response.status_code, 200)
