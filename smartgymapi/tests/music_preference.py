from datetime import date, timedelta

from smartgymapi.tests import FunctionalTestCase


class BusynessTest(FunctionalTestCase):

    def setUp(self):
        self.music_preference_id = 'df3cfe69-cf67-44bc-9c0e-f40226f8177d'
        super().setUp()

    def test_list_music_preferences(self):
        response = self.test_app.get('/music_preference',
                                     status=200)

    def test_get_music_preference(self):
        response = self.test_app.get('/music_preference/{}'
                                     .format(self.music_preference_id),
                                     status=200)

    def test_get_todays_busyness(self):
        response = self.test_app.post('/music_preference',
                                      {'genre': 'dance'},
                                      status=200)

    def get_predicted_busyness(self):
        tomorrow = date.today() + timedelta(1)
        response = self.test_app.get('/busyness/predict&gym_id={}&date={}'
                                     .format(self.gym_id,
                                             tomorrow.strftime('%y-%m-%d')),
                                     status=200)
