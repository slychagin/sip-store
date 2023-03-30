import time

from django import forms
from django.test import TestCase, tag
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from orders.forms import OrderForm


class OrderFormTest(TestCase):
    """Tests OrderForm"""

    @classmethod
    def setUpTestData(cls):
        """Create OrderForm"""
        cls.form = OrderForm()

    def test_form_fields_label(self):
        """Tests all labels in OrderForm"""
        self.assertTrue(
            self.form.fields['customer_name'].label is None
            or self.form.fields['customer_name'].label == 'ПІБ '
        )
        self.assertTrue(
            self.form.fields['phone'].label is None
            or self.form.fields['phone'].label == 'Телефон '
        )
        self.assertTrue(
            self.form.fields['email'].label is None
            or self.form.fields['email'].label == 'Email '
        )
        self.assertTrue(
            self.form.fields['city'].label is None
            or self.form.fields['city'].label == 'Місто '
        )
        self.assertTrue(
            self.form.fields['street'].label is None
            or self.form.fields['street'].label == 'Вулиця '
        )
        self.assertTrue(
            self.form.fields['house'].label is None
            or self.form.fields['house'].label == 'Будинок '
        )
        self.assertTrue(
            self.form.fields['room'].label is None
            or self.form.fields['room'].label == 'Квартира'
        )
        self.assertTrue(
            self.form.fields['new_post_city'].label is None
            or self.form.fields['new_post_city'].label == 'Виберіть місто доставки '
        )
        self.assertTrue(
            self.form.fields['new_post_office'].label is None
            or self.form.fields['new_post_office'].label == 'Виберiть вiддiлення '
        )

    def test_form_fields_title(self):
        """Tests all form fields titles"""
        for field in self.form.fields:
            self.assertEqual(
                self.form.fields[field].widget.attrs['title'],
                'Заповніть це поле'
            )

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
        """Tests that form is valid"""
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


@tag('selenium')
class OrderFormSeleniumTest(StaticLiveServerTestCase):
    """Test Order Form by Selenium"""
    selenium = None

    @classmethod
    def setUpClass(cls):
        """Setup Firefox webdriver"""
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        """Shutdown webdriver"""
        cls.selenium.quit()
        super().tearDownClass()

    def test_order_form_by_selenium(self):
        """Emulate filling and submit order form by user"""
        self.selenium.get(f'{self.live_server_url}/order/')
        time.sleep(1)

        customer_name_input = self.selenium.find_element(By.NAME, 'customer_name')
        phone_input = self.selenium.find_element(By.NAME, 'phone')
        email_input = self.selenium.find_element(By.NAME, 'email')
        city_input = self.selenium.find_element(By.NAME, 'city')
        street_input = self.selenium.find_element(By.NAME, 'street')
        house_input = self.selenium.find_element(By.NAME, 'house')

        time.sleep(5)

        submit = self.selenium.find_element(By.ID, 'order-btn')

        customer_name_input.send_keys('Sergio')
        phone_input.send_keys('+38(099)777-77-77')
        email_input.send_keys('email@gmail.com')
        city_input.send_keys('Boston')
        street_input.send_keys('st. Street')
        house_input.send_keys('25')

        submit.send_keys(Keys.RETURN)
