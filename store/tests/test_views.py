from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from category.models import Category
from store.models import Product
from store.views import store, product_details


class StoreViewTest(TestCase):
    """Tests Store view"""

    def setUp(self):
        """Create category and product object"""
        self.c = Client()
        self.factory = RequestFactory()
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')
        self.product_data = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category_id=1
        )

    def test_store_view_url_exists_at_desired_location(self):
        """Tests that store view url exists at desired location"""
        response = self.c.get('/store/')
        self.assertEqual(response.status_code, 200)

    def test_store_view_url_accessible_by_name(self):
        """Tests store view url accessible by name"""
        response = self.c.get(reverse('store'))
        self.assertEqual(response.status_code, 200)

    def test_store_view_uses_correct_template(self):
        """Tests store view uses correct template"""
        response = self.c.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_store_view_function(self):
        """Test home view function"""
        category_data = self.category_data
        product_data = self.product_data
        request = self.factory.get('/store/')
        response = store(request)
        html = response.content.decode('utf8')

        self.assertIn(str(category_data), html)
        self.assertIn(str(product_data), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_store_view_context(self):
        """Tests store view context"""
        response = self.c.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['category_links']) == 1)
        self.assertTrue(len(response.context['product_links']) == 1)
        self.assertTrue(len(response.context['products']) == 1)
        self.assertTrue(response.context['product_count'] == 1)


class ProductDetailsViewTest(TestCase):
    """Tests ProductDetail view"""

    def setUp(self):
        """Create category and product object"""
        self.c = Client()
        self.factory = RequestFactory()
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')
        self.product_data = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category_id=1
        )

    def test_product_detail_view_url_exists_at_desired_location(self):
        """Tests that product detail view url exists at desired location"""
        response = self.c.get('/store/chicken/fitness-chicken/')
        self.assertEqual(response.status_code, 200)

    def test_product_details_view_url_accessible_by_name(self):
        """Tests product details view url accessible by name"""
        response = self.c.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        self.assertEqual(response.status_code, 200)

    def test_product_details_view_uses_correct_template(self):
        """Tests product details view uses correct template"""
        response = self.c.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_details.html')

    def test_store_view_function(self):
        """Test home view function"""
        category_data = self.category_data
        product_data = self.product_data
        request = self.factory.get('/store/chicken/fitness-chicken/')
        response = product_details(request, 'chicken', 'fitness-chicken')
        html = response.content.decode('utf8')

        self.assertIn(str(category_data), html)
        self.assertIn(str(product_data), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_product_details_view_context(self):
        """Tests product details view context"""
        response = self.c.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('single_product' in response.context)
        self.assertEqual(response.context['single_product'].product_name, 'fitness chicken')
