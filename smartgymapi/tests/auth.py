from smartgymapi.lib.encrypt import hash_password, check_password
from smartgymapi.test import TestCase


class EncryptTest(TestCase):
    def setUp(self):
        super().setUp(self)

        self.test_password = 'test123'

    def test_hash_password(self):
        hashed_password, salt = hash_password(self.test_password)
        self.assertIsNotNone(self.hashed_password)
        self.assertIsNotNone(self.salt)

    def test_check_password(self):
        salt = '$2b$12$X2xgb/JItJpDL7RKfZhqwu'
        hashed_password = '$2b$12$X2xgb/JItJpDL7RKfZhqwubNVnj4onQS'\
            'Qio8ECMHzXjizx4gqn1Rq'
        self.assertTrue(check_password('test123', hashed_password, salt))
        self.asssertFalse(check_password('notrightpass', hashed_password,
                                         salt))
