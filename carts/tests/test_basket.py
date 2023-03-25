from importlib import import_module

from django.conf import settings
from django.test import TestCase, Client, RequestFactory

from carts.basket import Basket
from category.models import Category
from store.models import Product


class BasketTest(TestCase):
    """Tests Basket class"""

    @classmethod
    def setUpTestData(cls):
        """Create category and products"""
        cls.client = Client()
        cls.factory = RequestFactory()

        category = Category.objects.create(category_name='chicken', slug='chicken')
        cls.product_1 = Product.objects.create(
            product_name='chicken', slug='chicken', price=100,
            product_image='chicken', category=category
        )
        cls.product_2 = Product.objects.create(
            product_name='pork', slug='pork',
            price=200, product_image='pork', category=category
        )

    def setUp(self):
        """Create request and session"""
        self.request = self.factory
        self.engine = import_module(settings.SESSION_ENGINE)
        self.session = self.request.session = self.engine.SessionStore()

    def test_basket_add(self):
        """Tests add function"""

        # Get basket for particular session
        basket = Basket(self.request)

        # Add products to the basket and check that they are there
        basket.add(self.product_1, 1)
        basket.add(self.product_2, 2)
        cart = self.session.get('basket')
        self.assertIn(str(self.product_1.id), cart)
        self.assertIn(str(self.product_2.id), cart)

        # Check if products in basket than updates prices
        basket = Basket(self.request)

        # Add products to the basket, check quantity and basket size
        basket.add(self.product_1, 2)
        basket.add(self.product_2, 3)
        cart = self.session.get('basket')
        self.assertEqual(cart[str(self.product_1.id)]['qty'], 3)
        self.assertEqual(cart[str(self.product_2.id)]['qty'], 5)
        self.assertEqual(len([item for item in basket]), 2)

        # Check that item total price calculates correctly
        self.assertEqual(
            [item for item in basket][0]['total_price'],
            3 * self.product_1.price
        )
        self.assertEqual(
            [item for item in basket][1]['total_price'],
            5 * self.product_2.price
        )

    def test_basket_length(self):
        """Tests total product quantity in the basket"""
        basket = Basket(self.request)
        basket.add(self.product_1, 1)
        basket.add(self.product_2, 2)

        self.assertEqual(basket.__len__(), 3)

    def test_basket_get_total_price(self):
        """Tests basket get total sum"""
        basket = Basket(self.request)
        basket.add(self.product_1, 1)
        basket.add(self.product_2, 2)

        total_sum = self.product_1.price * 1 + self.product_2.price * 2
        self.assertEqual(basket.get_total_price(), total_sum)

    def test_basket_get_item_quantity(self):
        """Tests that basket get item quantity"""
        basket = Basket(self.request)
        basket.add(self.product_1, 5)
        basket.add(self.product_2, 3)

        self.assertEqual(basket.get_item_quantity(self.product_1.id), 5)

    def test_basket_get_sub_total(self):
        """Tests basket get sub total (qty * product.price)"""
        basket = Basket(self.request)
        basket.add(self.product_1, 2)
        basket.add(self.product_2, 3)

        product_1_sub_total = self.product_1.price * 2
        product_2_sub_total = self.product_2.price * 3
        self.assertEqual(basket.get_sub_total(self.product_1.id), product_1_sub_total)
        self.assertEqual(basket.get_sub_total(self.product_2.id), product_2_sub_total)

    def test_basket_add_quantity(self):
        """Tests that basket adds quantity by one"""
        basket = Basket(self.request)
        basket.add(self.product_1, 5)
        basket.add(self.product_2, 3)
        cart = self.session.get('basket')

        basket.add_quantity(self.product_1.id)
        basket.add_quantity(self.product_2.id)

        self.assertEqual(cart[str(self.product_1.id)]['qty'], 6)
        self.assertEqual(cart[str(self.product_2.id)]['qty'], 4)

    def test_basket_subtract_quantity(self):
        """Tests that basket decrease quantity by one"""
        basket = Basket(self.request)
        basket.add(self.product_1, 5)
        basket.add(self.product_2, 3)
        cart = self.session.get('basket')

        basket.subtract_quantity(self.product_1.id)
        basket.subtract_quantity(self.product_2.id)

        self.assertEqual(cart[str(self.product_1.id)]['qty'], 4)
        self.assertEqual(cart[str(self.product_2.id)]['qty'], 2)

    def test_basket_delete_item(self):
        """Tests that basket deletes item"""
        basket = Basket(self.request)
        basket.add(self.product_1, 1)
        basket.add(self.product_2, 1)
        cart = self.session.get('basket')

        basket.delete(self.product_2.id)

        with self.assertRaises(KeyError):
            print(cart[str(self.product_2.id)])

    def test_set_discount(self):
        """Tests that discount saves in the session"""
        basket = Basket(self.request)
        basket.set_discount(discount=10)

        self.assertIn('discount', self.session)
        self.assertEqual(self.session['discount'], 10)
