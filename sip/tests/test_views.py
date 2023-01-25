from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from sip.views import home
from category.models import Category
from store.models import Product


class ViewResponsesTest(TestCase):
    """Tests view responses in sip app"""

    def setUp(self):
        """Create category and product object"""
        self.c = Client()
        self.factory = RequestFactory()
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')
        self.product_data = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category_id=1
        )

    def test_url_allowed_hosts(self):
        """Test allowed hosts"""
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_category_url(self):
        """Test allowed category url"""
        response = self.c.get(reverse('products_by_category', args=['chicken']))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """Test allowed product detail url"""
        response = self.c.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """Test homepage html"""
        request = HttpRequest()
        response = home(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Сіль і Пательня</title>', html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_function(self):
        """Test home view function"""
        request = self.factory.get('/')
        response = home(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Сіль і Пательня</title>', html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

