import os
from importlib import import_module

from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import (
    TestCase,
    Client,
    RequestFactory
)

from orders.models import Subscribers
from sip.settings import BASE_DIR
from sip.views import HomePageView
from category.models import Category
from store.models import Product, ProductGallery


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
            price=120, product_image='good chicken', category=self.category
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
        response = self.client.get(
            reverse('products_by_category', args=['chicken'])
        )
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """Test allowed product detail url"""
        response = self.client.get(
            reverse('product_details', args=['chicken', 'fitness-chicken'])
        )
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


class GetSingleProductTest(TestCase):
    """Tests get single product function"""

    def setUp(self):
        """Create category, products and product gallery objects"""
        self.client = Client()

        # Create category and products
        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product_1 = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=100, product_image='good chicken', category=self.category
        )
        self.product_2 = Product.objects.create(
            product_name='pork', slug='pork',
            price=200, product_image='good pork', category=self.category
        )

        # Open image file for testing ProductGallery
        with open(os.path.join(BASE_DIR, 'sip/static/img/paypal.jpg'), "rb") as image_file:
            self.image = SimpleUploadedFile(image_file.name, image_file.read())

        # Product gallery objects
        # With video
        self.product_gallery_1 = ProductGallery.objects.create(
            product=self.product_1,
            image=self.image,
            video='https://www.youtube.com'
        )
        # Without video
        self.product_gallery_2 = ProductGallery.objects.create(
            product=self.product_2,
            image=self.image,
            video=''
        )

    def test_get_single_product(self):
        """Test get single product function"""
        # After press quick show button get data from database and throw ajax
        # show this data in product details popup window

        # With video
        response = self.client.post(
            reverse('get_single_product'),
            {'product_id': self.product_1.id, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(response.json()['title'], self.product_1.product_name)
        self.assertEqual(response.json()['price'], self.product_1.price)
        self.assertEqual(response.json()['product_url'], self.product_1.get_url())
        self.assertEqual(response.json()['image_main'], self.product_1.product_image.url)
        self.assertEqual(response.json()['target'], '_blank')

        # Without video
        response = self.client.post(
            reverse('get_single_product'),
            {'product_id': self.product_2.id, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(response.json()['video1'], self.product_2.get_url())
        self.assertEqual(response.json()['target'], '_self')


class SubscribeTest(TestCase):
    """Tests subscribe function"""

    def setUp(self):
        """Create email object"""
        self.client = Client()
        self.subscriber = Subscribers.objects.create(email='sergio@gmail.com')

    def test_subscribe_function(self):
        """Test subscribe function"""

        # Enter no valid email
        response = self.client.post(
            reverse('subscribe'),
            {'email': 'email', 'action': 'POST'},
            xhr=True
        )
        self.assertRaises(ValidationError)
        self.assertEqual(response.json()['error'], 'Введіть коректну email адресу')

        # Enter valid existing email
        response = self.client.post(
            reverse('subscribe'),
            {'email': 'sergio@gmail.com', 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(response.json()['success'], 'Ви вже підписувались.')

        # Enter valid not existing email
        response = self.client.post(
            reverse('subscribe'),
            {'email': 'mail@gmail.com', 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(response.json()['success'], 'Ви підписані!')
