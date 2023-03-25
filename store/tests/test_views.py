from importlib import import_module

from django.conf import settings
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from category.models import Category
from store.forms import ProductsSortForm
from store.models import Product
from store.views import (
    StorePageView,
    ProductsByCategoryListView,
    ProductDetailView
)


class StorePageViewTest(TestCase):
    """Tests StorePageView"""

    def setUp(self):
        """Create category and product object"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = StorePageView()

        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=120, product_image='good chicken', category=self.category
        )

    def test_store_page_view_url_exists_at_desired_location(self):
        """Tests that store view url exists at desired location"""
        response = self.client.get('/store/')
        self.assertEqual(response.status_code, 200)

    def test_store_page_view_url_accessible_by_name(self):
        """Tests store view url accessible by name"""
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)

    def test_store_page_view_uses_correct_template(self):
        """Tests store view uses correct template"""
        response = self.client.get(reverse('store'))
        self.assertTemplateUsed(response, 'store/store.html')

    def test_store_page_html(self):
        """Test StorePage html"""
        request = self.factory.get('/store/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf-8')

        self.assertIn(str(self.category), html)
        self.assertIn(str(self.product), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_store_page_view_context(self):
        """Tests StorePageView context"""
        request = self.factory.get('/store/')
        self.view.setup(request)
        context = self.view.get_context_data()

        self.assertTrue(len(context['products']) == 1)
        self.assertTrue(context['product_count'] == 1)
        self.assertTrue(isinstance(context['form'], ProductsSortForm))


class ProductsByCategoryListViewTest(TestCase):
    """Tests ProductsByCategoryListView class-based view"""

    def setUp(self):
        """Create category and product object"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = ProductsByCategoryListView()
        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=120, product_image='good chicken', category=self.category
        )

    def test_products_by_category_list_view_url_exists_at_desired_location(self):
        """Tests that products by category view url exists at desired location"""
        response = self.client.get('/store/category/chicken/')
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_list_view_url_accessible_by_name(self):
        """Tests products by category view url accessible by name"""
        response = self.client.get(reverse('products_by_category', args=['chicken']))
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_list_view_uses_correct_template(self):
        """Tests product by category view uses correct template"""
        response = self.client.get(reverse('products_by_category', args=['chicken']))
        self.assertTemplateUsed(response, 'store/store.html')

    def test_products_by_category_list_view(self):
        """Test product by category view"""
        request = self.factory.get('/store/chicken/')
        self.view.setup(request)
        response = self.client.get(reverse('products_by_category', args=['chicken']))
        html = response.content.decode('utf8')

        self.assertIn(str(self.category), html)
        self.assertIn(str(self.product), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_list_view_context(self):
        """Tests product by category view context"""
        response = self.client.get(reverse('products_by_category', args=['chicken']))
        context = response.context

        self.assertTrue(len(context['products']) == 1)
        self.assertTrue(context['product_count'] == 1)
        self.assertEqual(response.status_code, 200)


class ProductDetailViewTest(TestCase):
    """Tests ProductDetailView class-based view"""

    def setUp(self):
        """Create category and product object"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = ProductDetailView()

        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=120, product_image='good chicken', category=self.category
        )

    def test_product_detail_view_url_exists_at_desired_location(self):
        """Tests that product detail view url exists at desired location"""
        response = self.client.get('/store/category/chicken/fitness-chicken/')
        self.assertEqual(response.status_code, 200)

    def test_product_details_view_url_accessible_by_name(self):
        """Tests product details view url accessible by name"""
        response = self.client.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        self.assertEqual(response.status_code, 200)

    def test_product_details_view_uses_correct_template(self):
        """Tests product details view uses correct template"""
        response = self.client.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_details.html')

    def test_product_detail_view(self):
        """Test product detail class-based view"""
        request = self.factory.get('/store/chicken/fitness-chicken/')
        self.view.setup(request)
        response = self.client.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        html = response.content.decode('utf8')

        self.assertIn(str(self.category), html)
        self.assertIn(str(self.product), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_context(self):
        """Tests product detail view context"""
        response = self.client.get(
            reverse('product_details', args=['chicken', 'fitness-chicken'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('single_product' in response.context)
        self.assertEqual(response.context['single_product'].product_name, 'fitness chicken')

    def test(self):
        request = self.factory.get('/store/not-found/not-found/')
        self.view.setup(request)
        response = self.client.get(reverse('product_details', args=['chicken', 'fitness-chicken-not-found']))
        self.assertEqual(response.status_code, 404)
