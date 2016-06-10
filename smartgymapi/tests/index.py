from smartgymapi.test import FunctionalTestCase


class IndexTest(FunctionalTestCase):
    def test_get_view(self):
        response = self.test_app.get('/', status=200)
        self.assertTrue('version' in response.body)
