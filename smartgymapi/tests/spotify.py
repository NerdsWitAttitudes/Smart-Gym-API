from datetime import date, timedelta

from smartgymapi.tests import FunctionalTestCase


class BusynessTest(FunctionalTestCase):

    def setUp(self):
        self.gym_id = 'af425ccf-3eef-4f19-9e8d-8cb86867824e'
        super().setUp()

    def test_add_track(self):
        yesterday = date.today() - timedelta(1)
        response = self.test_app.get('/spotify&gym_id={}&date={}'
                                     .format(self.gym_id,
                                             yesterday.strftime('%y-%m-%d')),
                                     status=201)

    def test_delete_track(self):
        response = self.test_app.get('/spotify'
                                     .format(self.gym_id),
                                     status=204)
