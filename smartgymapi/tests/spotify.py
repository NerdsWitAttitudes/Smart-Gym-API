from smartgymapi.tests import FunctionalTestCase


class BusynessTest(FunctionalTestCase):

    def setUp(self):
        self.gym_id = 'af425ccf-3eef-4f19-9e8d-8cb86867824e'
        super().setUp()

    def test_add_track(self):
        response = self.test_app.post(
            '/spotify',
            {'client_address': '24:FD:52:E6:0F:FB'},
            status=201)

    def test_delete_track(self):
        response = self.test_app.get(
            '/spotify',
            {'uri':
             'spotify:track:06VFJ6o6ywoSdrSWMZMIoN',
             'client_address': '24:FD:52:E6:0F:FB'},
            status=204)
