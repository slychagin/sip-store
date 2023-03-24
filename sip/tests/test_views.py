from importlib import import_module

from django.conf import settings
from django.test import (
    TestCase,
    Client,
    RequestFactory
)
from django.urls import reverse

from sip.views import HomePageView
from category.models import Category
from store.models import Product


class HomePageTest(TestCase):
    """Tests HomePageView"""

    def setUp(self):
        """Create category and product objects"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = HomePageView()

        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category=self.category
        )

    def test_context_data_set_in_context(self):
        """Tests HomePageView by setting contex data in context"""
        request = self.factory.get('/')
        self.view.setup(request)
        context = self.view.get_context_data()

        context_list = [
            'main_banner', 'benefits', 'bestsellers', 'new_products', 'popular_left',
            'popular_center', 'popular_right', 'partners', 'week_offer_banners',
            'two_banners', 'offer_single_banner', 'footer_banner'
        ]

        for item in context_list:
            self.assertIn(item, context)

    def test_url_allowed_hosts(self):
        """Test allowed hosts"""
        response = self.client.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.client.get('/', HTTP_HOST='my-domain.com')
        self.assertEqual(response.status_code, 200)

    def test_category_url(self):
        """Test allowed category url"""
        response = self.client.get(reverse('products_by_category', args=['chicken']))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """Test allowed product detail url"""
        response = self.client.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """Test homepage html"""
        request = self.factory.get('/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf-8')

        self.assertIn('<title>Сіль і Пательня</title>', html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)
