from django.test import TestCase

from category.models import Category


class CategoryModelTest(TestCase):
    """Testing Category model"""

    @classmethod
    def setUpTestData(cls):
        """Create Category object"""
        cls.category_data = Category.objects.create(category_name='chicken', slug='chicken')

    def test_category_model_entry(self):
        """Test Category model data insertion/types/field attributes"""
        data = self.category_data
        self.assertTrue(isinstance(data, Category))

    def test_category_model_name(self):
        """Test Category name"""
        data = self.category_data
        self.assertEqual(str(data), 'chicken')

    def test_get_absolute_url(self):
        """Test absolute url for category object"""
        data = self.category_data
        self.assertEqual(data.get_url(), '/store/category/chicken/')

    def test_category_fields_max_length(self):
        """Test category fields max length"""
        data = self.category_data
        category_name_max_length = data._meta.get_field('category_name').max_length
        slug_max_length = data._meta.get_field('slug').max_length

        self.assertEqual(category_name_max_length, 100)
        self.assertEqual(slug_max_length, 255)

    def test_category_fields_label(self):
        """Test Category fields verbose name"""
        data = self.category_data

        category_name = data._meta.get_field('category_name').verbose_name
        slug = data._meta.get_field('slug').verbose_name
        description = data._meta.get_field('description').verbose_name
        category_image = data._meta.get_field('category_image').verbose_name

        self.assertEqual(category_name, 'найменування категорії')
        self.assertEqual(slug, 'написання в URL')
        self.assertEqual(description, 'опис')
        self.assertEqual(category_image, 'фото категорії')
