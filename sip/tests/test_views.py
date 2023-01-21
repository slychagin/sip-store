from django.test import TestCase


class UrlTest(TestCase):

    def test_home_page(self):
        """Test home page rendering"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

