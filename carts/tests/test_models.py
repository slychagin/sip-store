from datetime import date

from django.test import TestCase

from carts.models import Coupon


class CouponModelTest(TestCase):
    """Tests Coupon model"""

    @classmethod
    def setUpTestData(cls):
        """Create Coupon object"""
        cls.coupon = Coupon.objects.create(
            coupon_kod='aaa', discount=10, validity=date.today()
        )

    def test_coupon_entry(self):
        """Test Coupon model data insertion/types/field attributes"""
        data = self.coupon
        self.assertTrue(isinstance(data, Coupon))

    def test_coupon_model_name(self):
        """Tests Coupon object name"""
        data = self.coupon
        self.assertEqual(str(data), 'aaa')

    def test_coupon_fields_max_length(self):
        """Test Coupon fields max length"""
        data = self.coupon
        coupon_kod_max_length = data._meta.get_field('coupon_kod').max_length
        description_max_length = data._meta.get_field('description').max_length

        self.assertEqual(coupon_kod_max_length, 15)
        self.assertEqual(description_max_length, 255)

    def test_coupon_labels(self):
        """Test Coupon verbose names"""
        data = self.coupon

        coupon_kod = data._meta.get_field('coupon_kod').verbose_name
        discount = data._meta.get_field('discount').verbose_name
        validity = data._meta.get_field('validity').verbose_name
        is_available = data._meta.get_field('is_available').verbose_name
        description = data._meta.get_field('description').verbose_name
        created_date = data._meta.get_field('created_date').verbose_name
        modified_date = data._meta.get_field('modified_date').verbose_name

        self.assertEqual(coupon_kod, 'промокод')
        self.assertEqual(discount, 'знижка, %')
        self.assertEqual(validity, 'термін дії')
        self.assertEqual(is_available, 'знижка доступна')
        self.assertEqual(description, 'опис')
        self.assertEqual(created_date, 'дата створення')
        self.assertEqual(modified_date, 'дата змін')
