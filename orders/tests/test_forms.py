from django import forms
from django.test import TestCase

from orders.forms import OrderForm


class OrderFormTest(TestCase):
    """Tests OrderForm"""

    def test_form_fields_label(self):
        """Tests all labels in PostCommentForm"""
        form = OrderForm()
        self.assertTrue(form.fields['customer_name'].label is None or form.fields['customer_name'].label == 'ПІБ ')
        self.assertTrue(form.fields['phone'].label is None or form.fields['phone'].label == 'Телефон ')
        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'Email ')
        self.assertTrue(form.fields['city'].label is None or form.fields['city'].label == 'Місто ')
        self.assertTrue(form.fields['street'].label is None or form.fields['street'].label == 'Вулиця ')
        self.assertTrue(form.fields['house'].label is None or form.fields['house'].label == 'Будинок ')
        self.assertTrue(form.fields['room'].label is None or form.fields['room'].label == 'Квартира')
        self.assertTrue(form.fields['new_post_city'].label is None or form.fields['new_post_city'].label == 'Виберіть місто доставки ')
        self.assertTrue(form.fields['new_post_office'].label is None or form.fields['new_post_office'].label == 'Виберiть вiддiлення ')

    def test_form_fields_title(self):
        """Tests all form fields titles"""
        form = OrderForm()
        for field in form.fields:
            self.assertEqual(
                form.fields[field].widget.attrs['title'],
                'Заповніть це поле')

    def test_clean_customer_name(self):
        """
        Tests that the username does not contain numbers,
        punctuation marks, and does not consist of a single letter
        """
        form = OrderForm(data={
            'order_number': '500',
            'customer_name': '1',
            'phone': '+38(066)777-77-77',
            'email': 'mail@gmail.ru',
            'city': 'Boston',
            'street': 'st. Street',
            'house': '25',
            'order_total': 500,
            'discount': 20
        })
        self.assertFalse(form.is_valid())
        self.assertRaises(forms.ValidationError)

    def test_valid_form(self):
        """
        Tests that form is valid
        """
        form = OrderForm(data={
            'order_number': '500',
            'customer_name': 'Sergio',
            'phone': '+38(066)777-77-77',
            'email': 'mail@gmail.ru',
            'city': 'Boston',
            'street': 'st. Street',
            'house': '25',
            'new_post_city': 'New_York',
            'new_post_office': '25',
            'delivery_method': 'COURIER_CHERKASY',
            'payment_method': 'CASH',
            'order_total': 500,
            'discount': 20
        })
        self.assertTrue(form.is_valid())
