from django.test import TestCase

from benefits.models import Benefits, Partners


class BenefitsModelTest(TestCase):
    """Testing Benefits model"""

    def setUp(self):
        """Create Benefits object"""
        self.benefits_data = Benefits.objects.create(
            title='title', description='description', image='image'
        )

    def test_benefits_model_entry(self):
        """Test Benefits model data insertion/types/field attributes"""
        data = self.benefits_data
        self.assertTrue(isinstance(data, Benefits))

    def test_benefits_model_name(self):
        """Test Benefits name"""
        data = self.benefits_data
        self.assertEqual(str(data), 'title')

    def test_benefits_title_label(self):
        """Test Benefits title verbose name"""
        data = self.benefits_data
        field_label = data._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Заголовок')

    def test_benefits_description_label(self):
        """Test benefits description verbose name"""
        data = self.benefits_data
        field_label = data._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Опис')

    def test_benefits_image_label(self):
        """Test benefits image verbose name"""
        data = self.benefits_data
        field_label = data._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'Фото переваги')

    def test_benefits_title_max_length(self):
        """Test benefits title max length"""
        data = self.benefits_data
        max_length = data._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_benefits_description_max_length(self):
        """Test benefits description max length"""
        data = self.benefits_data
        max_length = data._meta.get_field('description').max_length
        self.assertEqual(max_length, 255)


class PartnersModelTest(TestCase):
    """Testing Partners model"""

    def setUp(self):
        """Create Partners object"""
        self.partners_data = Partners.objects.create(title='title', image='image')

    def test_partners_model_entry(self):
        """Test Partners model data insertion/types/field attributes"""
        data = self.partners_data
        self.assertTrue(isinstance(data, Partners))

    def test_partners_model_name(self):
        """Test Partners name"""
        data = self.partners_data
        self.assertEqual(str(data), 'title')

    def test_partners_title_label(self):
        """Test Partners title verbose name"""
        data = self.partners_data
        field_label = data._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Найменування партнеру')

    def test_partners_image_label(self):
        """Test Partners image verbose name"""
        data = self.partners_data
        field_label = data._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'Фото партнера')

    def test_partners_title_max_length(self):
        """Test partners title max length"""
        data = self.partners_data
        max_length = data._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)
