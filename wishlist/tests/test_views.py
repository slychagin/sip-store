from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from category.models import Category
from store.models import Product
from wishlist.views import WishlistPageView


class WishlistPageViewTest(TestCase):
    """Tests WishlistPageView"""

    @classmethod
    def setUpTestData(cls):
        """Create category, product and user objects"""
        cls.client = Client()
        cls.factory = RequestFactory()
        cls.view = WishlistPageView()

        User.objects.create(username='admin')
        category = Category.objects.create(category_name='chicken', slug='chicken')
        cls.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=100, product_image='good chicken', category=category
        )

    def setUp(self):
        """Add created in setUpTestData products to the wishlist"""
        self.client.post(
            reverse('add_wishlist'),
            {'product_id': self.product.id, 'action': 'POST'},
            xhr=True
        )

    def test_wishlist_page_view_url_exists_at_desired_location(self):
        """Tests that wishlist page view url exists at desired location"""
        response = self.client.get('/wishlist/')
        self.assertEqual(response.status_code, 200)

    def test_wishlist_page_view_url_accessible_by_name(self):
        """Tests wishlist view url accessible by name"""
        response = self.client.get(reverse('wish'))
        self.assertEqual(response.status_code, 200)

    def test_wishlist_page_view_uses_correct_template(self):
        """Tests wishlist view uses correct template"""
        response = self.client.get(reverse('wish'))
        self.assertTemplateUsed(response, 'store/wishlist.html')

    def test_wishlist_page_html(self):
        """Test WishlistPage html"""
        request = self.factory.get('/wishlist/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf-8')

        self.assertIn(str(self.product), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_wishlist_page_view_context(self):
        """Tests WishlistPageView context"""
        request = self.factory.get('/wishlist/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        context = self.view.get_context_data()

        self.assertIn('wishlist', context)

    def test_wishlist_add(self):
        """Test adding items to the wishlist"""
        response = self.client.post(
            reverse('add_wishlist'),
            {'product_id': self.product.id, 'action': 'POST'},
            xhr=True
        )

        self.assertEqual(response.json(), {'qty': 1})

    def test_wishlist_delete(self):
        """Test deleting items from the wishlist"""

        response = self.client.post(
            reverse('wishlist_delete'),
            {'product_id': self.product.id, 'action': 'POST'},
            xhr=True
        )

        self.assertEqual(response.json(), {'qty': 0})
