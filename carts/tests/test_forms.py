import datetime

from django import forms
from django.test import TestCase

from carts.forms import CouponAdminForm


class CouponAdminFormTest(TestCase):
    """Tests CouponAdminForm"""

    def test_clean_required_fields(self):
        """Tests that admin entered validity date and discount"""
        form = CouponAdminForm(data={'coupon_kod': 'AAA'})
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Це поле обов'язкове.")

    def test_clean_validity_date(self):
        """Tests that admin entered validity date > date.today()"""
        date_in_the_past = datetime.date.today() - datetime.timedelta(days=1)
        form = CouponAdminForm(data={
            'coupon_kod': 'AAA',
            'discount': 20,
            'validity': date_in_the_past
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            forms.ValidationError, 'Введіть дату більш ніж сьогоднішня дата.'
        )

    def test_clean_discount(self):
        """Tests that admin entered discount from 1% to 100%"""
        invalid_discounts = [-20, 120]
        for discount in invalid_discounts:
            form = CouponAdminForm(data={
                'coupon_kod': 'AAA',
                'discount': discount,
                'validity': datetime.date.today()
            })
            self.assertFalse(form.is_valid())
            self.assertRaisesMessage(
                forms.ValidationError,
                'Введіть знижку від 1 до 100 відсотків'
            )

    def test_valid_form(self):
        """Tests that form is valid"""
        form = CouponAdminForm(data={
            'coupon_kod': 'AAA',
            'discount': 20,
            'validity': datetime.date.today()
        })
        self.assertTrue(form.is_valid())
