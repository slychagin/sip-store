import time

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from contacts.forms import ContactForm


class ContactFormTest(TestCase):
    """Tests ContactForm"""

    def test_form_fields_label(self):
        """Tests all labels in ContactForm"""
        form = ContactForm()
        self.assertTrue(
            form.fields['name'].label is None
            or form.fields['name'].label == "Ім'я"
        )
        self.assertTrue(
            form.fields['email'].label is None
            or form.fields['email'].label == 'Електронна пошта'
        )
        self.assertTrue(
            form.fields['title'].label is None
            or form.fields['title'].label == 'Тема'
        )
        self.assertTrue(
            form.fields['title'].label is None
            or form.fields['message'].label == 'Повідомлення'
        )

    def test_form_fields_max_length(self):
        """Tests all fields max length"""
        form = ContactForm()
        self.assertEqual(form.fields['name'].max_length, 100)
        self.assertEqual(form.fields['email'].max_length, 100)
        self.assertEqual(form.fields['title'].max_length, 200)

    def test_form_fields_placeholder(self):
        """Tests all fields placeholders"""
        form = ContactForm()
        self.assertEqual(
            form.fields['name'].widget.attrs['placeholder'],
            "Введіть Ваше ім'я"
        )
        self.assertEqual(
            form.fields['email'].widget.attrs['placeholder'],
            'Введіть Вашу електронну пошту'
        )
        self.assertEqual(
            form.fields['title'].widget.attrs['placeholder'],
            'Введіть тему повідомлення'
        )
        self.assertEqual(
            form.fields['message'].widget.attrs['placeholder'],
            'Текст повідомлення'
        )

    def test_form_fields_title(self):
        """Tests all form fields titles"""
        form = ContactForm()
        for field in form.fields:
            self.assertEqual(
                form.fields[field].widget.attrs['title'],
                'Заповніть це поле')

    def test_form_clean_message_greater_2000_sings(self):
        """Tests message validation field by length"""
        text = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla egestas elit turpis,
            sit amet luctus nisl suscipit ac. Donec non purus eu arcu sodales sodales ac eu leo.
            Mauris eleifend quis metus dapibus congue. Etiam tincidunt, libero ac venenatis
            tempus, ipsum neque pellentesque neque, et euismod purus nisi vel lectus. Donec
            imperdiet ut ante ut feugiat. Aliquam interdum eget nisi ut pellentesque. Mauris
            tincidunt semper lorem in blandit. Quisque vel mi quam. Ut eu urna posuere,
            ultricies ipsum nec, rhoncus justo. Curabitur viverra nulla vel justo euismod,
            id tincidunt mi fringilla. Ut tempor et mauris ac placerat. Ut pellentesque
            luctus enim, dapibus tempor tortor vulputate vel. Donec eu commodo ante.
            Vestibulum sagittis, neque sed dignissim maximus, dui neque facilisis velit,
            in laoreet est risus a sapien. Vivamus at elit id augue congue accumsan quis
            nec nibh. Sed sed mollis turpis. Phasellus feugiat justo dui, malesuada posuere
            ligula porta nec. Vivamus condimentum elit justo quam.
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla egestas elit turpis,
            sit amet luctus nisl suscipit ac. Donec non purus eu arcu sodales sodales ac eu leo.
            Mauris eleifend quis metus dapibus congue. Etiam tincidunt, libero ac venenatis
            tempus, ipsum neque pellentesque neque, et euismod purus nisi vel lectus. Donec
            imperdiet ut ante ut feugiat. Aliquam interdum eget nisi ut pellentesque. Mauris
            tincidunt semper lorem in blandit. Quisque vel mi quam. Ut eu urna posuere,
            ultricies ipsum nec, rhoncus justo. Curabitur viverra nulla vel justo euismod,
            id tincidunt mi fringilla. Ut tempor et mauris ac placerat. Ut pellentesque
            luctus enim, dapibus tempor tortor vulputate vel. Donec eu commodo ante.
            Vestibulum sagittis, neque sed dignissim.
        """

        form = ContactForm(data={
            'name': 'Serhio',
            'email': 'email@gmail.com',
            'title': 'Hello!',
            'message': text
        })
        self.assertFalse(form.is_valid())

    def test_form_clean_message_less_1000_sings(self):
        """Tests message validation field by length"""
        text = """
             Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla egestas
             elit turpis, sit amet luctus nisl suscipit ac.
        """

        form = ContactForm(data={
            'name': 'Serhio',
            'email': 'email@gmail.com',
            'title': 'Hello!',
            'message': text
        })
        self.assertTrue(form.is_valid())


class ContactFormSeleniumTest(StaticLiveServerTestCase):
    """Test ContactForm by Selenium"""
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

    def test_review_rating_form_by_selenium(self):
        """Emulate filling and submit ContactForm by user"""
        self.selenium.get(f'{self.live_server_url}/contacts/')
        time.sleep(2)

        name_input = self.selenium.find_element(By.NAME, 'name')
        email_input = self.selenium.find_element(By.NAME, 'email')
        title_input = self.selenium.find_element(By.NAME, 'title')
        message_input = self.selenium.find_element(By.NAME, 'message')
        time.sleep(2)

        submit = self.selenium.find_element(By.ID, 'ajax_contact')

        name_input.send_keys('Sergio')
        email_input.send_keys('email@gmail.com')
        title_input.send_keys('Hello!')
        message_input.send_keys('Lorem ipsum!')

        submit.send_keys(Keys.RETURN)
        time.sleep(2)
