import os
import unittest
from unittest.mock import Mock

from paste.deploy.loadwsgi import appconfig
from pyramid import testing
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from webtest import TestApp

from smartgymapi import main
from smartgymapi.models.meta import Base, DBSession as session

here = os.path.dirname(__file__)
settings = appconfig('config:{}'.format(os.path.join(here, '../../',
                     'test.ini')))


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker()

    def setUp(self):
        connection = self.engine.connect()
        connection.begin()

        session.configure(bind=connection)
        self.session = self.Session(bind=connection)

        Base.session = self.session

    def tearDown(self):
        session.remove()
        testing.tearDown()


class UnitTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.config = testing.setUp(request=testing.DummyRequest())

    def get_post_request(self, post=None):
        request = testing.DummyRequest(json_body=post)

        request.session = Mock()

        return request


class FunctionalTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.app = main({}, **settings)

    def setUp(self):
        super().setUp()
        self.app = TestApp(self.app)
        self.config = testing.setUp()
