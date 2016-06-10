from smartgymapi.tests import TestCase


class SimilarityTest(TestCase):
    def test_ordered_list_similarity(self):
        from smartgymapi.lib.similarity import get_ordered_list_similarity

        self.assertEqual(get_ordered_list_similarity([3, 2, 1], [3, 2, 1]), 1)
        self.assertNotEqual(get_ordered_list_similarity([3, 2, 1], [3, 2]), 1)
