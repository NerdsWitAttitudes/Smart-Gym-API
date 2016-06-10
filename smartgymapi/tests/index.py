from smartgymapi.tests import FunctionalTestCase


class IndexTest(FunctionalTestCase):
    def test_get_view(self):
        response = self.app.get('/', status=200)
        self.assertTrue(b'version' in response.body)
