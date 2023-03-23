from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from category.models import Category
from store.models import Product


class TestCartPageView(TestCase):
    """Tests CartPageView"""

    @classmethod
    def setUpTestData(cls):
        """Create category, product and user objects"""
        User.objects.create(username='admin')
        Category.objects.create(category_name='chicken', slug='chicken')
        Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category_id=1
        )
        Product.objects.create(
            product_name='good chicken', slug='good-chicken',
            price='120', product_image='good chicken', category_id=1
        )
        Product.objects.create(
            product_name='amazing chicken', slug='amazing-chicken',
            price='120', product_image='good chicken', category_id=1
        )

    def setUp(self):
        """Add created in setUpTestData products to the basket"""
        self.client.post(
            reverse('add_cart'),
            {'product_id': 1, 'quantity': 1, 'action': 'POST'},
            xhr=True
        )
        self.client.post(
            reverse('add_cart'),
            {'product_id': 2, 'quantity': 2, 'action': 'POST'},
            xhr=True
        )

    def test_cart_url(self):
        """Test cart page response status"""
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_cart_add(self):
        """Test adding items to the cart"""
        response = self.client.post(
            reverse('add_cart'), {'product_id': 3, 'quantity': 1, 'action': 'POST'}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('add_cart'), {'product_id': 2, 'quantity': 1, 'action': 'POST'}, xhr=True)
        self.assertEqual(response.json(), {'qty': 5})

    def test_cart_delete(self):
        """Test deleting items from the cart"""
        response = self.client.post(
            reverse('cart_delete'), {'product_id': 2, 'action': 'POST'}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'total': 120})

    def test_plus_quantity(self):
        """Test increase item by one"""
        response = self.client.post(
            reverse('plus_quantity'), {'product_id': 2, 'action': 'POST'}, xhr=True)
        self.assertEqual(
            response.json(),
            {'qty': 4, 'total': 480, 'item_qty': 3, 'item_total_price': 360}
        )

    def test_minus_quantity(self):
        """Test decrease item by one"""
        response = self.client.post(
            reverse('minus_quantity'), {'product_id': 2, 'action': 'POST'}, xhr=True)
        self.assertEqual(
            response.json(),
            {'qty': 2, 'total': 240, 'item_qty': 1, 'item_total_price': 120}
        )
        response = self.client.post(
            reverse('minus_quantity'), {'product_id': 2, 'action': 'POST'}, xhr=True)
        self.assertEqual(
            response.json(),
            {'qty': 1, 'total': 120, 'item_qty': 0, 'item_total_price': 0}
        )

    def test_mini_cart_delete(self):
        """Test deleting items from the mini cart"""
        response = self.client.post(
            reverse('mini_cart_delete'), {'product_id': 2, 'action': 'POST'}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'mini_cart_total': 120})
