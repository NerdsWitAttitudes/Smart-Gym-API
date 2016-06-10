from datetime import date, timedelta

from smartgymapi.tests import FunctionalTestCase


class BusynessTest(FunctionalTestCase):

    def setUp(self):
        self.gym_id = 'af425ccf-3eef-4f19-9e8d-8cb86867824e'
        super().setUp()

    def test_get_past_busyness(self):
        yesterday = date.today() - timedelta(1)
        response = self.app.get('/busyness/past&gym_id={}&date={}'
                                .format(self.gym_id,
                                        yesterday.strftime('%y-%m-%d')),
                                status=200)

    def test_get_todays_busyness(self):
        response = self.app.get('/busyness/today&gym_id={}'
                                .format(self.gym_id),
                                status=200)

    def get_predicted_busyness(self):
        tomorrow = date.today() + timedelta(1)
        response = self.app.get('/busyness/predict&gym_id={}&date={}'
                                .format(self.gym_id,
                                        tomorrow.strftime('%y-%m-%d')),
                                status=200)
