import unittest

from pyramid import testing


class TestCase(unittest.TestCase):
    def setUp(self):
        dummy_request = testing.DummyRequest()
        self.config = testing.setUp(request=dummy_request)

    def tearDown(self):
        testing.tearDown()


class FunctionalTestCase(unittest.TestCase):
    def setUp(self):
        from smartgymapi import main
        app = main({})
        from webtest import TestApp
        self.test_app = TestApp(app)
