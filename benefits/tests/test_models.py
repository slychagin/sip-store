from django.test import TestCase

from benefits.models import Benefits, Partners


class BenefitsModelTest(TestCase):
    """Tests the Benefits model"""

    @classmethod
    def setUpTestData(cls):
        """Create Benefits object"""
        cls.benefits_data = Benefits.objects.create(
            title='title', description='description', image='image'
        )

    def test_benefits_model_entry(self):
        """
        Test that created benefits object is
        instance of Benefit model
        """
        self.assertTrue(isinstance(self.benefits_data, Benefits))

    def test_benefits_model_name(self):
        """Test Benefits name"""
        self.assertEqual(str(self.benefits_data), 'title')

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
        """
        Test that created partners object is
        instance of Partner model
        """
        self.assertTrue(isinstance(self.partners_data, Partners))

    def test_partners_model_name(self):
        """Test Partners object name"""
        self.assertEqual(str(self.partners_data), 'title')

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

        self.assertEqual(title, 'найменування партнера')
        self.assertEqual(image, 'фото партнера')
