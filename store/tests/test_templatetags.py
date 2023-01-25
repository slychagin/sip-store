from django.test import TestCase

from store.templatetags.get_index import get_index


class GetIndexStoreTest(TestCase):
    """Testing store app templatetags"""

    def test_get_index(self):
        """Testing custom function get_index"""
        my_list = [0, 1, 2, 3]
        self.assertEqual(get_index(my_list, 3), 3)
