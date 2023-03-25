from importlib import import_module

from django.conf import settings
from django.test import TestCase, Client, RequestFactory

from category.models import Category
from store.models import Product
from wishlist.wishlist import Wishlist


class WishlistTest(TestCase):
    """Tests Wishlist class"""

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

    def test_add_wishlist(self):
        """Tests add to wishlist function"""

        # Get wishlist for particular session
        wishlist = Wishlist(self.request)

        # Add products to the wishlist and check that they are there
        wishlist.add_wishlist(self.product_1)
        wishlist.add_wishlist(self.product_2)
        wish_list = self.session.get('wishlist')
        self.assertIn(str(self.product_1.id), wish_list)
        self.assertIn(str(self.product_2.id), wish_list)

        # Check wishlist size
        self.assertEqual(len([item for item in wishlist]), 2)

    def test_wishlist_delete_item(self):
        """Tests that wishlist deletes item"""
        wishlist = Wishlist(self.request)
        wishlist.add_wishlist(self.product_1)
        wishlist.add_wishlist(self.product_2)
        wish_list = self.session.get('wishlist')

        wishlist.delete_wishlist(self.product_2.id)

        with self.assertRaises(KeyError):
            print(wish_list[str(self.product_2.id)])

    def test_wishlist_length(self):
        """Tests item quantity in the wishlist"""
        wishlist = Wishlist(self.request)
        wishlist.add_wishlist(self.product_1)
        wishlist.add_wishlist(self.product_2)

        self.assertEqual(wishlist.__len__(), 2)
