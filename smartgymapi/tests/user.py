import datetime

from pyramid import testing

from smartgymapi.tests import UnitTestCase


class TestUserHanders(UnitTestCase):
    def test_get(self):
        from smartgymapi.handlers.user import RESTUser
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

        request = testing.DummyRequest()
        request.context = user

        RESTUser(request).get()

        self.assertEqual(request.response.status_code, 200)

    def test_current_user(self):
        from smartgymapi.handlers.user import RESTUser
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

        request = testing.DummyRequest()
        request.user = user

        RESTUser(request).get_current_user()

        self.assertEqual(request.response.status_code, 200)

    def test_list(self):
        from webob.multidict import MultiDict
        from smartgymapi.handlers.user import RESTUser
        from smartgymapi.lib.factories.user import UserFactory
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
        user_2 = User(first_name='test',
                      last_name='person',
                      password_hash=hashed_password,
                      password_salt=salt,
                      email='testing@test.com',
                      country='The Netherlands',
                      date_of_birth=datetime.datetime.now())

        self.session.add(user)
        self.session.add(user_2)
        self.session.flush()

        request = testing.DummyRequest()
        request.GET = MultiDict()
        request.context = UserFactory(None, 'user')

        response = RESTUser(request).list()

        self.assertEqual(request.response.status_code, 200)

        self.assertIs(type(response), list)

    def test_post(self):
        from smartgymapi.handlers.user import RESTUser

        request_body = {
            "first_name": "new",
            "last_name": "person",
            "password": "testing123",
            "password_confirm": "testing123",
            "email": "new@user.com",
            "country": "The Netherlands",
            "date_of_birth": datetime.datetime.now().isoformat()
        }

        request = self.get_post_request(post=request_body)

        rest_user = RESTUser(request)
        rest_user.post()

        self.assertEqual(rest_user.request.response.status_code, 201)

    def test_put(self):
        from smartgymapi.handlers.user import RESTUser
        from smartgymapi.models.user import User

        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        request_body = {
            "first_name": "update_new",
            "last_name": "person",
            "password": "testing123",
            "password_confirm": "testing123",
            "email": "new@user.com",
            "country": "The Netherlands",
            "date_of_birth": datetime.datetime.now().isoformat()
        }

        request = self.get_post_request(post=request_body)

        user_3 = User(first_name='test',
                      last_name='person',
                      password_hash=hashed_password,
                      password_salt=salt,
                      email='tesadasdasst@test.com',
                      country='The Netherlands',
                      date_of_birth=datetime.datetime.now())

        self.session.add(user_3)
        self.session.flush()
        self.session.close()

        request.context = user_3
        rest_user = RESTUser(request)
        rest_user.put()

        self.assertEqual(rest_user.request.response.status_code, 200)

    def test_delete(self):
        from pyramid.httpexceptions import HTTPNoContent
        from smartgymapi.handlers.user import RESTUser
        from smartgymapi.models.user import User

        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'

        request = testing.DummyRequest()

        user_4 = User(first_name='test',
                      last_name='person',
                      password_hash=hashed_password,
                      password_salt=salt,
                      email='tesadasdasst@test.com',
                      country='The Netherlands',
                      date_of_birth=datetime.datetime.now())

        self.session.add(user_4)
        self.session.flush()
        self.session.close()

        request.context = user_4
        rest_user = RESTUser(request)

        self.assertRaises(HTTPNoContent, rest_user.delete)
