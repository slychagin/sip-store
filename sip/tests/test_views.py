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
        self.c = Client()
        self.factory = RequestFactory()
        self.view = HomePageView()

        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')
        self.product_data = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category_id=1
        )

    def test_context_data_set_in_context(self):
        """Tests HomePageView by setting contex data in context"""
        request = self.factory.get('/')
        self.view.setup(request)

        context = self.view.get_context_data()
        context_list = [
            'benefits', 'bestsellers', 'new_products', 'popular_left',
            'popular_center', 'popular_right', 'partners', 'week_offer_banners'
                        ]
        for item in context_list:
            self.assertIn(item, context)

    def test_url_allowed_hosts(self):
        """Test allowed hosts"""
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='my-domain.com')
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
        request = self.factory.get('/')
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf8')

        self.assertIn('<title>Сіль і Пательня</title>', html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)
