import os

from django import forms
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from category.models import Category
from sip.settings import BASE_DIR
from store.forms import ProductGalleryForm, ReviewRatingForm, ReviewRatingAdminForm, ProductsSortForm
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
        self.image_file = open(
            os.path.join(BASE_DIR, 'static/img/paypal.jpg'), "rb"
        )
        self.image = SimpleUploadedFile(self.image_file.name, self.image_file.read())

    def test_clean_image_video_not_entered(self):
        """
        Tests that admin not entered image and video
        """
        form = ProductGalleryForm(data={
            'product': self.product,
        })
        self.assertFalse(form.is_valid())
        self.assertRaises(forms.ValidationError)

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
        self.assertRaises(forms.ValidationError)

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

    def test_form_fields_label(self):
        """Tests all labels in ReviewRatingForm"""
        form = ReviewRatingForm()
        self.assertTrue(
            form.fields['name'].label is None
            or form.fields['name'].label == "Ім'я"
        )
        self.assertTrue(
            form.fields['email'].label is None
            or form.fields['email'].label == 'Email'
        )
        self.assertTrue(
            form.fields['review'].label is None
            or form.fields['review'].label == 'Ваш відгук'
        )

    def test_form_fields_title(self):
        """Tests all form fields titles"""
        form = ReviewRatingForm()
        for field in form.fields:
            self.assertEqual(
                form.fields[field].widget.attrs['title'],
                'Заповніть це поле')

    def test_clean_rating_equal_zero(self):
        """
        Tests that rating zero
        """
        form = ReviewRatingForm(data={
            'rating': 0,
            'review': 'Hello!',
            'name': 'Sergio',
            'email': 'email@gmail.com'
        })
        self.assertFalse(form.is_valid())
        self.assertRaises(forms.ValidationError)

    def test_clean_rating_not_zero(self):
        """
        Tests that rating not zero
        """
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
        self.assertRaises(forms.ValidationError)

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
