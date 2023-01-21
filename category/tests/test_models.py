from django.test import TestCase
from category.models import Category


class CategoryModelTest(TestCase):
    """Testing Category model"""

    @classmethod
    def setUpTestData(cls):
        """Create Category object"""
        Category.objects.create(category_name='chicken', slug='chicken')

    def test_category_model_entry(self):
        """Test Category model data insertion/types/field attributes"""
        data = Category.objects.get(id=1)
        self.assertTrue(isinstance(data, Category))

    def test_category_model_name(self):
        """Tests Category name"""
        data = Category.objects.get(id=1)
        self.assertEqual(str(data), 'chicken')

    def test_category_name_label(self):
        """Test Category verbose name"""
        data = Category.objects.get(id=1)
        field_label = data._meta.get_field('category_name').verbose_name
        self.assertEqual(field_label, 'Найменування категорії')

    def test_category_description_label(self):
        """Test Category description verbose name"""
        data = Category.objects.get(id=1)
        field_label = data._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Опис')

    def test_category_image_label(self):
        """Test Category image verbose name"""
        data = Category.objects.get(id=1)
        field_label = data._meta.get_field('category_image').verbose_name
        self.assertEqual(field_label, 'Фото категорії')

    def test_category_name_max_length(self):
        """Test category name max length"""
        data = Category.objects.get(id=1)
        max_length = data._meta.get_field('category_name').max_length
        self.assertEqual(max_length, 100)

    def test_category_slug_max_length(self):
        """Test category slug max length"""
        data = Category.objects.get(id=1)
        max_length = data._meta.get_field('slug').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_category_name(self):
        """Test object name"""
        data = Category.objects.get(id=1)
        expected_object_name = f'{data.category_name}'
        self.assertEqual(expected_object_name, str(data))


