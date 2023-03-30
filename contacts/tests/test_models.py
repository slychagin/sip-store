from django.test import TestCase

from contacts.models import SalePoint


class SalePointModelTest(TestCase):
    """Tests SalePoint model"""

    @classmethod
    def setUpTestData(cls):
        """Create SalePoint object"""
        cls.sale_point = SalePoint.objects.create(name='Sale Point')

    def test_sale_point_entry(self):
        """
        Test that created sale point object is
        instance of SalePoint model
        """
        self.assertTrue(isinstance(self.sale_point, SalePoint))

    def test_sale_point_model_name(self):
        """Tests SalePoint object name"""
        self.assertEqual(str(self.sale_point), 'Sale Point')

    def test_sale_point_max_length(self):
        """Test SalePoint fields max length"""
        data = self.sale_point

        name_max_length = data._meta.get_field('name').max_length
        city_max_length = data._meta.get_field('city').max_length
        street_max_length = data._meta.get_field('street').max_length
        house_max_length = data._meta.get_field('house').max_length
        corpus_max_length = data._meta.get_field('corpus').max_length
        latitude_max_length = data._meta.get_field('latitude').max_length
        longitude_max_length = data._meta.get_field('longitude').max_length
        mobile_phone_max_length = data._meta.get_field('mobile_phone').max_length
        city_phone_max_length = data._meta.get_field('city_phone').max_length
        email_max_length = data._meta.get_field('email').max_length
        schedule_max_length = data._meta.get_field('schedule').max_length

        self.assertEqual(name_max_length, 200)
        self.assertEqual(city_max_length, 100)
        self.assertEqual(street_max_length, 100)
        self.assertEqual(house_max_length, 10)
        self.assertEqual(corpus_max_length, 10)
        self.assertEqual(latitude_max_length, 50)
        self.assertEqual(longitude_max_length, 50)
        self.assertEqual(mobile_phone_max_length, 50)
        self.assertEqual(city_phone_max_length, 50)
        self.assertEqual(email_max_length, 100)
        self.assertEqual(schedule_max_length, 200)

    def test_sale_point_labels(self):
        """Test SalePoint verbose names"""
        data = self.sale_point

        name = data._meta.get_field('name').verbose_name
        description = data._meta.get_field('description').verbose_name
        city = data._meta.get_field('city').verbose_name
        street = data._meta.get_field('street').verbose_name
        house = data._meta.get_field('house').verbose_name
        corpus = data._meta.get_field('corpus').verbose_name
        latitude = data._meta.get_field('latitude').verbose_name
        longitude = data._meta.get_field('longitude').verbose_name
        mobile_phone = data._meta.get_field('mobile_phone').verbose_name
        city_phone = data._meta.get_field('city_phone').verbose_name
        email = data._meta.get_field('email').verbose_name
        schedule = data._meta.get_field('schedule').verbose_name
        image = data._meta.get_field('image').verbose_name
        is_opened = data._meta.get_field('is_opened').verbose_name
        created = data._meta.get_field('created').verbose_name
        updated = data._meta.get_field('updated').verbose_name

        self.assertEqual(name, 'найменування точки продажу')
        self.assertEqual(description, 'опис')
        self.assertEqual(city, 'місто')
        self.assertEqual(street, 'вулиця')
        self.assertEqual(house, 'будинок')
        self.assertEqual(corpus, 'корпус')
        self.assertEqual(latitude, 'широта')
        self.assertEqual(longitude, 'довгота')
        self.assertEqual(mobile_phone, 'мобільний телефон')
        self.assertEqual(city_phone, 'міський телефон')
        self.assertEqual(email, 'E-mail')
        self.assertEqual(schedule, 'графік роботи')
        self.assertEqual(image, 'фото')
        self.assertEqual(is_opened, 'працює')
        self.assertEqual(created, 'дата замовлення')
        self.assertEqual(updated, 'дата коригування')
