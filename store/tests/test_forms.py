import os
import time

from django import forms
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, tag
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from category.models import Category
from orders.models import Order, OrderItem
from sip.settings import BASE_DIR
from store.forms import (
    ProductGalleryForm,
    ProductsSortForm,
    ReviewRatingAdminForm,
    ReviewRatingForm,
)
from store.models import Product, ReviewRating


class ProductGalleryFormTest(TestCase):
    """Tests ProductGalleryForm"""

    def setUp(self):
        """Create product object"""
        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=120, product_image='good chicken', category=self.category
        )

        # Open image file for testing ProductGallery
        with open(os.path.join(BASE_DIR, 'sip/static/img/paypal.jpg'), "rb") as image_file:
            self.image = SimpleUploadedFile(image_file.name, image_file.read())

    def test_clean_image_video_not_entered(self):
        """
        Tests that admin not entered image and video
        """
        form = ProductGalleryForm(data={
            'product': self.product,
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            forms.ValidationError,
            'Треба ввести або фото або відео!'
        )

    def test_clean_image_video_entered_together(self):
        """
        Tests that admin entered image and video together
        """
        form = ProductGalleryForm(
            data={
                'product': self.product,
                'video': """
                https://www.youtube.com/watch?v=cBUk1pemshU&ab_channel=%D0%9A%D1%83%D1%85%D0%BD%D1%8F
%D0%BD%D0%B0%D0%BB%D1%8E%D0%B1%D0%BE%D0%B9%D0%B2%D0%BA%D1%83%D1%81%D1%81%D0%95%D0%BB%D0%B5%D0%BD%D0%BE%D0%B9%D0%A3%
                """
            },
            files={
                'image': self.image
            }
        )
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            forms.ValidationError,
            'Введіть щось одне - або фото або відео!'
        )

    def test_clean_image_video_entered_one_of_them(self):
        """
        Tests that admin entered or image or video
        """
        form = ProductGalleryForm(
            data={
                'product': self.product
            },
            files={
                'image': self.image
            }
        )
        self.assertTrue(form.is_valid())


class ReviewRatingFormTest(TestCase):
    """Tests ReviewRatingForm"""

    def setUp(self):
        """Create ReviewRatingForm"""
        self.form = ReviewRatingForm()

    def test_form_fields_label(self):
        """Tests all labels in ReviewRatingForm"""
        self.assertTrue(
            self.form.fields['name'].label is None
            or self.form.fields['name'].label == "Ім'я"
        )
        self.assertTrue(
            self.form.fields['email'].label is None
            or self.form.fields['email'].label == 'Email'
        )
        self.assertTrue(
            self.form.fields['review'].label is None
            or self.form.fields['review'].label == 'Ваш відгук'
        )

    def test_form_fields_title(self):
        """Tests all form fields titles"""
        for field in self.form.fields:
            self.assertEqual(
                self.form.fields[field].widget.attrs['title'],
                'Заповніть це поле')

    def test_clean_rating_equal_zero(self):
        """Tests when rating zero"""
        form = ReviewRatingForm(data={
            'rating': 0,
            'review': 'Hello!',
            'name': 'Sergio',
            'email': 'email@gmail.com'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            forms.ValidationError,
            'Будь ласка, встановіть рейтинг'
        )

    def test_clean_rating_not_zero(self):
        """Tests when rating not zero"""
        form = ReviewRatingForm(data={
            'rating': 5.0,
            'review': 'Hello!',
            'name': 'Sergio',
            'email': 'email@gmail.com'
        })
        self.assertTrue(form.is_valid())


class ReviewRatingAdminFormTest(TestCase):
    """Tests ReviewRatingAdminForm"""

    def setUp(self):
        """Create blog category, post and post comment objects"""
        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=120, product_image='good chicken', category=self.category
        )
        self.post_comment = ReviewRating.objects.create(
            product=self.product, rating=5.0, review='Hello',
            name='Sergio', email='email@gmail.com'
        )

    def test_clean_method_invalid_form(self):
        """
        Tests that form rase error if administrator entered
        review for product in admin panel with not unique email
        """
        form = ReviewRatingAdminForm(data={
            'product': self.product,
            'rating': 5.0,
            'review': 'Hello',
            'name': 'Sergio',
            'email': 'email@gmail.com'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            forms.ValidationError,
            'Відгук з таким email по даному товару вже існує.'
        )

    def test_clean_method_valid_form(self):
        """
        Tests that form valid if administrator entered
        review for product in admin panel with unique email
        """
        form = ReviewRatingAdminForm(data={
            'product': self.product,
            'rating': 5.0,
            'review': 'Hello',
            'name': 'Sergio',
            'email': 'sergio@gmail.com'
        })
        self.assertTrue(form.is_valid())


class ProductsSortFormTest(TestCase):
    """Tests ProductsSortForm"""

    def test_products_sort_form(self):
        """Tests ProductsSortForm"""
        choices = ['id', 'pk', '-count_orders', 'rating', 'price', '-price']

        form = ProductsSortForm()
        form_choices = [choice[0] for choice in form.CHOICES]

        for choice in choices:
            self.assertIn(choice, form_choices)


@tag('selenium')
class ReviewRatingFormSeleniumTest(StaticLiveServerTestCase):
    """Test ReviewRatingForm by Selenium"""
    selenium = None

    def setUp(self):
        """Create category, product, order and order item objects"""
        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=200, product_image='good chicken', category=self.category
        )
        self.order = Order.objects.create(
            order_number='200', customer_name='Sergio', phone='+38(099)777-77-77',
            email='email@gmail.com', city='Boston', street='st. Street',
            house='12', order_total=200, discount=50
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, price=self.product.price,
            is_ordered=True, user_email='email@gmail.com'
        )

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
        """Emulate filling and submit ReviewRatingForm by user"""
        self.selenium.get(
            f'{self.live_server_url}/store/category/{self.category.slug}/{self.product.slug}/'
        )
        time.sleep(2)

        self.selenium.find_element(By.ID, 'reviews-tab').click()
        time.sleep(1)

        star_radio_button = self.selenium.find_element(By.CSS_SELECTOR, "input[type='radio'][value='3']")
        review_input = self.selenium.find_element(By.NAME, 'review')
        name_input = self.selenium.find_element(By.NAME, 'name')
        email_input = self.selenium.find_element(By.NAME, 'email')
        time.sleep(2)

        submit = self.selenium.find_element(By.ID, 'ajax_review')

        self.selenium.execute_script("$(arguments[0]).click();", star_radio_button)
        review_input.send_keys('Super post!')
        name_input.send_keys('Sergio')
        email_input.send_keys('email@gmail.com')

        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        new_review = ReviewRating.objects.all()[0]
        self.assertTrue(new_review)
