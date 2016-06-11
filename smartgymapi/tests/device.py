import datetime
import uuid

from pyramid import testing

from smartgymapi.tests import UnitTestCase


class TestDeviceHanders(UnitTestCase):
    def test_list(self):
        from smartgymapi.handlers.device import DeviceHandler
        from smartgymapi.lib.factories.device import DeviceFactory
        from smartgymapi.models.device import Device
        from smartgymapi.models.user import User
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

        device_1 = Device(name='test device',
                          device_address='D8:96:95:22:EB:5F',
                          device_class=7995916,
                          user_id=user_id)
        device_2 = Device(name='test device2',
                          device_address='14:F4:2A:83:B4:01',
                          device_class=7995916,
                          user_id=user_id)
        self.session.add(device_1)
        self.session.add(device_2)
        self.session.flush()

        request = testing.DummyRequest()
        device_factory = DeviceFactory(None, 'devices')
        device_factory.request = request
        request.context = device_factory
        request.user = user

        device_handler = DeviceHandler(request)
        response = device_handler.list()

        self.assertEqual(request.response.status_code, 200)

        self.assertIs(type(response), list)

    def test_post(self):
        from smartgymapi.handlers.device import DeviceHandler
        from smartgymapi.lib.factories.device import DeviceFactory
        from smartgymapi.models.user import User
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

        body = {
            "name": 'test device',
            "device_address": 'D2:96:95:22:EB:5F',
            "device_class": 7995916,
        }

        self.session.flush()
        self.session.close()

        request = self.get_post_request(post=body)
        device_factory = DeviceFactory(None, 'devices')
        device_factory.request = request
        request.context = device_factory
        request.user = user

        device_handler = DeviceHandler(request)
        device_handler.post()

        self.assertEqual(request.response.status_code, 201)

    def test_delete(self):
        from pyramid.httpexceptions import HTTPNoContent
        from smartgymapi.handlers.device import DeviceHandler
        from smartgymapi.models.device import Device
        from smartgymapi.models.user import User
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

        device = Device(name='test device',
                        device_address='D8:92:95:22:EB:5F',
                        device_class=7995916,
                        user_id=user_id)
        self.session.add(device)
        self.session.flush()
        self.session.close()

        request = testing.DummyRequest()
        request.context = device
        request.user = user

        device_handler = DeviceHandler(request)
        self.assertRaises(HTTPNoContent, device_handler.delete)
