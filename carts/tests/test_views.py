from datetime import date
from importlib import import_module

from django.conf import settings
from django.contrib.auth.models import User
from django.test import (
    TestCase,
    Client,
    RequestFactory
)
from django.urls import reverse

from carts.models import Coupon
from carts.views import CartPageView
from category.models import Category
from store.models import Product


class CartPageViewTest(TestCase):
    """Tests CartPageView"""

    @classmethod
    def setUpTestData(cls):
        """Create category, product and user objects"""
        cls.client = Client()
        cls.factory = RequestFactory()
        cls.view = CartPageView()

        User.objects.create(username='admin')
        category = Category.objects.create(category_name='chicken', slug='chicken')
        cls.product_1 = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=120, product_image='good chicken', category=category
        )
        cls.product_2 = Product.objects.create(
            product_name='good chicken', slug='good-chicken',
            price=120, product_image='good chicken', category=category
        )
        cls.coupon = Coupon.objects.create(
            coupon_kod='AAA', discount=20, validity=date.today()
        )

    def setUp(self):
        """Add created in setUpTestData products to the basket"""
        self.client.post(
            reverse('add_cart'),
            {'product_id': self.product_1.id, 'quantity': 1, 'action': 'POST'},
            xhr=True
        )
        self.client.post(
            reverse('add_cart'),
            {'product_id': self.product_2.id, 'quantity': 2, 'action': 'POST'},
            xhr=True
        )

    def test_cart_page_view_url_exists_at_desired_location(self):
        """Tests that cart page view url exists at desired location"""
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_cart_page_view_url_accessible_by_name(self):
        """Tests cart view url accessible by name"""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_cart_page_view_uses_correct_template(self):
        """Tests cart view uses correct template"""
        response = self.client.get(reverse('cart'))
        self.assertTemplateUsed(response, 'store/cart.html')

    def test_cart_page_html(self):
        """Test CartPage html"""
        request = self.factory.get('/cart/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf-8')

        self.assertIn(str(self.product_1), html)
        self.assertIn(str(self.product_2), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_cart_page_view_context(self):
        """Tests CartPageView context"""
        request = self.factory.get('/cart/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        context = self.view.get_context_data()

        self.assertIn('basket', context)

    def test_cart_add(self):
        """Test adding items to the cart"""
        response = self.client.post(
            reverse('add_cart'),
            {'product_id': self.product_1.id, 'quantity': 1, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('add_cart'),
            {'product_id': self.product_2.id, 'quantity': 1, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(response.json(), {'qty': 5})

    def test_cart_delete(self):
        """Test deleting items from the cart"""
        response = self.client.post(
            reverse('cart_delete'),
            {'product_id': self.product_2.id, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(response.json(), {'qty': 1, 'total': 120})

    def test_plus_quantity(self):
        """Test increase item by one"""
        response = self.client.post(
            reverse('plus_quantity'),
            {'product_id': self.product_2.id, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(
            response.json(),
            {'qty': 4, 'total': 480, 'item_qty': 3, 'item_total_price': 360}
        )

    def test_minus_quantity(self):
        """Test decrease item by one"""
        response = self.client.post(
            reverse('minus_quantity'),
            {'product_id': self.product_2.id, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(
            response.json(),
            {'qty': 2, 'total': 240, 'item_qty': 1, 'item_total_price': 120}
        )
        response = self.client.post(
            reverse('minus_quantity'),
            {'product_id': self.product_2.id, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(
            response.json(),
            {'qty': 1, 'total': 120, 'item_qty': 0, 'item_total_price': 0}
        )

    def test_mini_cart_delete(self):
        """Test deleting items from the mini cart"""
        response = self.client.post(
            reverse('mini_cart_delete'),
            {'product_id': self.product_1.id, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(response.json(), {'qty': 2, 'mini_cart_total': 240})

    def test_get_coupon(self):
        """Tests checking valid or invalid coupon"""
        total_without_coupon = self.product_1.price * 1 + self.product_2.price * 2
        cart_discount = int(20 * total_without_coupon / 100)
        total = total_without_coupon - cart_discount

        # Test valid coupon
        response = self.client.post(
            reverse('get_coupon'),
            {'coupon': 'aaa', 'action': 'POST'},
            xhr=True
        )

        self.assertEqual(response.json(), {
            'cart_discount': cart_discount,
            'total': total,
            'coupon_discount': 20
        })

        # Test invalid coupon
        response = self.client.post(
            reverse('get_coupon'),
            {'coupon': 'bbb', 'action': 'POST'},
            xhr=True
        )

        self.assertEqual(response.json(), {
            'cart_discount': 0,
            'total': total_without_coupon
        })
