from django.test import TestCase

from category.models import Category
from store.models import Product


class ProductModelTest(TestCase):
    """Testing Product model"""

    def setUp(self):
        """Create Product object"""
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')
        self.product_data = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category_id=1
        )

    def test_product_model_entry(self):
        """Test Product model data insertion/types/field attributes"""
        data = self.product_data
        self.assertTrue(isinstance(data, Product))

    def test_product_model_name(self):
        """Tests Product name"""
        data = self.product_data
        self.assertEqual(str(data), 'fitness chicken')

    def test_product_name_label(self):
        """Test Product verbose name"""
        data = self.product_data
        field_label = data._meta.get_field('product_name').verbose_name
        self.assertEqual(field_label, 'Найменування товару')

    def test_product_description_label(self):
        """Test Product description verbose name"""
        data = self.product_data
        field_label = data._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Опис')

    def test_product_image_label(self):
        """Test Product image verbose name"""
        data = self.product_data
        field_label = data._meta.get_field('product_image').verbose_name
        self.assertEqual(field_label, 'Фото товару')

    def test_object_name_is_product_name(self):
        """Test object name"""
        data = self.product_data
        expected_object_name = f'{data.product_name}'
        self.assertEqual(expected_object_name, str(data))

    def test_product_name_max_length(self):
        """Test product name max length"""
        data = self.product_data
        max_length = data._meta.get_field('product_name').max_length
        self.assertEqual(max_length, 255)

    def test_product_slug_max_length(self):
        """Test product slug max length"""
        data = self.product_data
        max_length = data._meta.get_field('slug').max_length
        self.assertEqual(max_length, 255)

    def test_product_price_is_integer(self):
        """Test product price"""
        data = self.product_data
        product_price = data._meta.get_field('price')
        self.assertTrue(type(product_price), int)

    def test_get_url(self):
        """Test absolute url for product object"""
        data = self.product_data
        self.assertEqual(data.get_url(), '/store/chicken/fitness-chicken/')
