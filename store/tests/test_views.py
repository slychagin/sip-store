from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from category.models import Category
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
        self.c = Client()
        self.factory = RequestFactory()
        self.view = StorePageView()

        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')
        self.product_data = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category_id=1
        )

    def test_store_page_view_url_exists_at_desired_location(self):
        """Tests that store view url exists at desired location"""
        response = self.c.get('/store/')
        self.assertEqual(response.status_code, 200)

    def test_store_page_view_url_accessible_by_name(self):
        """Tests store view url accessible by name"""
        response = self.c.get(reverse('store'))
        self.assertEqual(response.status_code, 200)

    def test_store_page_view_uses_correct_template(self):
        """Tests store view uses correct template"""
        response = self.c.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_store_page_class_based_view(self):
        """Test StorePage class-based view"""
        category_data = self.category_data
        product_data = self.product_data
        request = self.factory.get('/store/')
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf8')

        self.assertIn(str(category_data), html)
        self.assertIn(str(product_data), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_store_page_view_context(self):
        """Tests StorePageView context"""
        response = self.c.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['category_links']) == 1)
        self.assertTrue(len(response.context['product_links']) == 1)
        self.assertTrue(len(response.context['products']) == 1)
        self.assertTrue(response.context['product_count'] == 1)


class ProductsByCategoryListViewTest(TestCase):
    """Tests ProductsByCategoryListView class-based view"""

    def setUp(self):
        """Create category and product object"""
        self.c = Client()
        self.factory = RequestFactory()
        self.view = ProductsByCategoryListView()
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')
        self.product_data = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category_id=1
        )

    def test_products_by_category_list_view_url_exists_at_desired_location(self):
        """Tests that products by category view url exists at desired location"""
        response = self.c.get('/store/category/chicken/')
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_list_view_url_accessible_by_name(self):
        """Tests products by category view url accessible by name"""
        response = self.c.get(reverse('products_by_category', args=['chicken']))
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_list_view_uses_correct_template(self):
        """Tests product by category view uses correct template"""
        response = self.c.get(reverse('products_by_category', args=['chicken']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_products_by_category_list_view(self):
        """Test product by category view"""
        category_data = self.category_data
        product_data = self.product_data
        request = self.factory.get('/store/chicken/')
        self.view.setup(request)
        response = self.c.get(reverse('products_by_category', args=['chicken']))
        html = response.content.decode('utf8')

        self.assertIn(str(category_data), html)
        self.assertIn(str(product_data), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_list_view_context(self):
        """Tests product by category view context"""
        response = self.c.get(reverse('products_by_category', args=['chicken']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('category_links' in response.context)


class ProductDetailViewTest(TestCase):
    """Tests ProductDetailView class-based view"""

    def setUp(self):
        """Create category and product object"""
        self.c = Client()
        self.factory = RequestFactory()
        self.view = ProductDetailView()
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')
        self.product_data = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category_id=1
        )

    def test_product_detail_view_url_exists_at_desired_location(self):
        """Tests that product detail view url exists at desired location"""
        response = self.c.get('/store/category/chicken/fitness-chicken/')
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

    def test_product_detail_view(self):
        """Test product detail class-based view"""
        category_data = self.category_data
        product_data = self.product_data
        request = self.factory.get('/store/chicken/fitness-chicken/')
        self.view.setup(request)
        response = self.c.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        html = response.content.decode('utf8')

        self.assertIn(str(category_data), html)
        self.assertIn(str(product_data), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_context(self):
        """Tests product detail view context"""
        response = self.c.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('single_product' in response.context)
        self.assertEqual(response.context['single_product'].product_name, 'fitness chicken')

    def test(self):
        request = self.factory.get('/store/not-found/not-found/')
        self.view.setup(request)
        response = self.c.get(reverse('product_details', args=['chicken', 'fitness-chicken-not-found']))
        self.assertEqual(response.status_code, 404)
