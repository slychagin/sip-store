from django.test import TestCase

from benefits.models import Benefits, Partners


class BenefitsModelTest(TestCase):
    """Testing Benefits model"""

    @classmethod
    def setUpTestData(cls):
        """Create Benefits object"""
        cls.benefits_data = Benefits.objects.create(
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

    def test_benefits_fields_max_length(self):
        """Test benefits fields max length"""
        data = self.benefits_data
        title_max_length = data._meta.get_field('title').max_length
        description_max_length = data._meta.get_field('description').max_length

        self.assertEqual(title_max_length, 100)
        self.assertEqual(description_max_length, 255)

    def test_benefits_fields_label(self):
        """Test Benefits fields verbose name"""
        data = self.benefits_data

        title = data._meta.get_field('title').verbose_name
        description = data._meta.get_field('description').verbose_name
        image = data._meta.get_field('image').verbose_name

        self.assertEqual(title, 'заголовок')
        self.assertEqual(description, 'опис')
        self.assertEqual(image, 'фото переваги')


class PartnersModelTest(TestCase):
    """Testing Partners model"""

    @classmethod
    def setUpTestData(cls):
        """Create Partners object"""
        cls.partners_data = Partners.objects.create(title='title', image='image')

    def test_partners_model_entry(self):
        """Test Partners model data insertion/types/field attributes"""
        data = self.partners_data
        self.assertTrue(isinstance(data, Partners))

    def test_partners_model_name(self):
        """Test Partners object name"""
        data = self.partners_data
        self.assertEqual(str(data), 'title')

    def test_partners_fields_max_length(self):
        """Test partners fields max length"""
        data = self.partners_data
        title_max_length = data._meta.get_field('title').max_length
        self.assertEqual(title_max_length, 100)

    def test_partners_fields_label(self):
        """Test Partners fields verbose name"""
        data = self.partners_data
        title = data._meta.get_field('title').verbose_name
        image = data._meta.get_field('image').verbose_name

        self.assertEqual(title, 'найменування партнеру')
        self.assertEqual(image, 'фото партнера')
