from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from carts.basket import Basket
from category.models import Category
from store.models import (
    Product,
    ProductGallery,
    ProductInfo,
    ReviewRating,
    count_products
)


class ProductModelTest(TestCase):
    """Tests Product model"""

    @classmethod
    def setUpTestData(cls):
        """Create Product object"""
        category = Category.objects.create(category_name='chicken', slug='chicken')
        cls.product_1 = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=120, product_image='good chicken', category=category
        )
        cls.product_2 = Product.objects.create(
            product_name='beacon', slug='beacon',
            price=220, product_image='beacon', category=category
        )
        cls.product_3 = Product.objects.create(
            product_name='pork', slug='pork',
            price=320, product_image='pork', category=category
        )

    def test_product_model_entry(self):
        """
        Test that created Product object is
        instance of Product model
        """
        self.assertTrue(isinstance(self.product_1, Product))

    def test_product_model_name(self):
        """Tests Product name"""
        self.assertEqual(str(self.product_1), 'fitness chicken')

    def test_get_url(self):
        """Test absolute url for product object"""
        self.assertEqual(
            self.product_1.get_url(),
            '/store/category/chicken/fitness-chicken/'
        )

    def test_average_review_rating(self):
        """Test calculating average review rating"""
        product_1_ratings = [1.5, 2.5, 3.5]  # 7.5/3 = 2.5 -> 2.5
        product_2_ratings = [3.0, 2.0, 3.5]  # 8.5/3 = 2.83 - 2 = 0.83 -> 2.5
        product_3_ratings = [1.5, 2.0, 3.5]  # 7/3 = 2.33 - 2 = 0.33 -> 2.0

        for rating in product_1_ratings:
            ReviewRating.objects.create(
                product=self.product_1, rating=rating, review='Good product!',
                name='Serhio', email='gmail@gmail.com', is_moderated=True
            )
        for rating in product_2_ratings:
            ReviewRating.objects.create(
                product=self.product_2, rating=rating, review='Bad product!',
                name='Serhio', email='gmail@gmail.com', is_moderated=True
            )
        for rating in product_3_ratings:
            ReviewRating.objects.create(
                product=self.product_3, rating=rating, review='Good product!',
                name='Serhio', email='gmail@gmail.com', is_moderated=True
            )

        self.assertEqual(self.product_1.average_review_rating(), 2.5)
        self.assertEqual(self.product_2.average_review_rating(), 2.5)
        self.assertEqual(self.product_3.average_review_rating(), 2.0)

    def test_product_fields_max_length(self):
        """Test product fields max length"""
        data = self.product_1
        product_name_max_length = data._meta.get_field('product_name').max_length
        slug_max_length = data._meta.get_field('slug').max_length
        unit_max_length = data._meta.get_field('unit').max_length
        related_products_title_max_length = data._meta.get_field('related_products_title').max_length

        self.assertEqual(product_name_max_length, 255)
        self.assertEqual(slug_max_length, 255)
        self.assertEqual(unit_max_length, 50)
        self.assertEqual(related_products_title_max_length, 255)

    def test_product_price_is_integer(self):
        """Test product price"""
        product_price = self.product_1._meta.get_field('price')
        self.assertTrue(type(product_price), int)

    def test_product_labels(self):
        """Test Product verbose names"""
        data = self.product_1

        product_name = data._meta.get_field('product_name').verbose_name
        slug = data._meta.get_field('slug').verbose_name
        short_description = data._meta.get_field('short_description').verbose_name
        description = data._meta.get_field('description').verbose_name
        specification = data._meta.get_field('specification').verbose_name
        price = data._meta.get_field('price').verbose_name
        price_old = data._meta.get_field('price_old').verbose_name
        weight = data._meta.get_field('weight').verbose_name
        unit = data._meta.get_field('unit').verbose_name
        product_image = data._meta.get_field('product_image').verbose_name
        second_image = data._meta.get_field('second_image').verbose_name
        is_available = data._meta.get_field('is_available').verbose_name
        is_new = data._meta.get_field('is_new').verbose_name
        is_sale = data._meta.get_field('is_sale').verbose_name
        created_date = data._meta.get_field('created_date').verbose_name
        modified_date = data._meta.get_field('modified_date').verbose_name
        count_orders = data._meta.get_field('count_orders').verbose_name
        category = data._meta.get_field('category').verbose_name
        related_products_title = data._meta.get_field('related_products_title').verbose_name
        related_products = data._meta.get_field('related_products').verbose_name

        self.assertEqual(product_name, 'найменування товару')
        self.assertEqual(slug, 'написання в URL')
        self.assertEqual(short_description, 'короткий опис')
        self.assertEqual(description, 'детальний опис')
        self.assertEqual(specification, 'специфікація')
        self.assertEqual(price, 'ціна')
        self.assertEqual(price_old, 'стара ціна')
        self.assertEqual(weight, 'вага, кг')
        self.assertEqual(unit, 'одиниця виміру')
        self.assertEqual(product_image, 'активне фото')
        self.assertEqual(second_image, 'друге фото')
        self.assertEqual(is_available, 'доступний')
        self.assertEqual(is_new, 'new')
        self.assertEqual(is_sale, 'sale')
        self.assertEqual(created_date, 'дата створення')
        self.assertEqual(modified_date, 'дата змін')
        self.assertEqual(count_orders, 'замовлено одиниць')
        self.assertEqual(category, 'категорія')
        self.assertEqual(related_products_title, 'заголовок до супутніх товарів')
        self.assertEqual(related_products, 'супутні товари')


class CountProductsTest(TestCase):
    """Tests count product function in Product model"""

    def setUp(self):
        """Add created in setUpTestData products to the basket"""
        self.factory = RequestFactory()

        category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product_1 = Product.objects.create(
            product_name='chicken', slug='chicken', price=100,
            product_image='good chicken', category=category
        )
        self.product_2 = Product.objects.create(
            product_name='pork', slug='pork', price=200,
            product_image='good pork', category=category
        )

        self.client.post(
            reverse('add_cart'),
            {'product_id': self.product_1.id, 'quantity': 1, 'action': 'POST'},
            xhr=True
        )
        self.client.post(
            reverse('add_cart'),
            {'product_id': self.product_2.id, 'quantity': 2, 'action': 'POST'},
            xhr=True
        )

    def test_count_products(self):
        """Test count products function"""
        response = self.client.get(reverse('cart'))
        request = response.wsgi_request
        basket = Basket(request)
        count_products(basket)
        self.product_1.refresh_from_db()
        self.product_2.refresh_from_db()

        self.assertEqual(self.product_1.count_orders, 1)
        self.assertEqual(self.product_2.count_orders, 2)


class ProductGalleryModelTest(TestCase):
    """Tests ProductGallery model"""

    @classmethod
    def setUpTestData(cls):
        """Create Product object"""
        category = Category.objects.create(category_name='chicken', slug='chicken')
        product = Product.objects.create(
            product_name='pork', slug='pork', price=100,
            product_image='good pork', category=category
        )
        cls.product_gallery = ProductGallery.objects.create(product=product)

    def test_product_gallery_entry(self):
        """
        Test that created ProductGallery object is
        instance of ProductGallery model
        """
        self.assertTrue(isinstance(self.product_gallery, ProductGallery))

    def test_product_gallery_model_name(self):
        """Tests ProductGallery object name"""
        self.assertEqual(str(self.product_gallery), 'pork')

    def test_product_gallery_fields_max_length(self):
        """Test ProductGallery fields max length"""
        image_max_length = self.product_gallery._meta.get_field('image').max_length
        self.assertEqual(image_max_length, 255)

    def test_product_gallery_labels(self):
        """Test ProductGallery verbose names"""
        data = self.product_gallery

        product = data._meta.get_field('product').verbose_name
        image = data._meta.get_field('image').verbose_name
        video = data._meta.get_field('video').verbose_name

        self.assertEqual(product, 'товар')
        self.assertEqual(image, 'фото')
        self.assertEqual(video, 'відео')


class ProductInfoModelTest(TestCase):
    """Tests ProductInfo model"""

    @classmethod
    def setUpTestData(cls):
        """Create ProductInfo object"""
        cls.product_info = ProductInfo.objects.create()

    def test_product_info_entry(self):
        """
        Test that created ProductInfo object is
        instance of ProductInfo model
        """
        self.assertTrue(isinstance(self.product_info, ProductInfo))

    def test_product_info_model_name(self):
        """Tests ProductInfo object name"""
        self.assertEqual(str(self.product_info), 'Інформація щодо товару')

    def test_product_info_labels(self):
        """Test ProductInfo verbose names"""
        description = self.product_info._meta.get_field('description').verbose_name
        self.assertEqual(description, 'інфо')


class ReviewRatingModelTest(TestCase):
    """Tests ReviewRating model"""

    def setUp(self):
        """Create ReviewRating object"""
        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='pork', slug='pork', price=100,
            product_image='good pork', category=self.category
        )
        self.review_rating = ReviewRating.objects.create(
            product=self.product, rating=4.5, review='A good product!',
            name='Serhio', email='gmail@gmail.com'
        )

    def test_review_rating_entry(self):
        """
        Test that created ReviewRating object is
        instance of ReviewRating model
        """
        self.assertTrue(isinstance(self.review_rating, ReviewRating))

    def test_review_rating_model_name(self):
        """Test ReviewRating object name"""
        self.assertEqual(str(self.review_rating), 'pork')

    def test_rating_validation(self):
        """
        Check rating that in should be from 0.5 to 5.0 with step 0.5
        """
        ReviewRating.objects.create(
            product=self.product, rating=0, review='A good product!',
            name='Serhio', email='gmail@gmail.com'
        )
        self.assertRaisesMessage(
            ValidationError,
            'Рейтинг повинен входити до діапазону від 0,5 до 5,0 з кроком 0,5')

        ReviewRating.objects.create(
            product=self.product, rating=5.5, review='A good product!',
            name='Serhio', email='gmail@gmail.com'
        )
        self.assertRaisesMessage(
            ValidationError,
            'Рейтинг повинен входити до діапазону від 0,5 до 5,0 з кроком 0,5')

        ReviewRating.objects.create(
            product=self.product, rating=3.3, review='A good product!',
            name='Serhio', email='gmail@gmail.com'
        )
        self.assertRaisesMessage(
            ValidationError,
            'Рейтинг повинен входити до діапазону від 0,5 до 5,0 з кроком 0,5')

    def test_review_rating_fields_max_length(self):
        """Test ReviewRating fields max length"""
        data = self.review_rating
        review_max_length = data._meta.get_field('review').max_length
        name_max_length = data._meta.get_field('name').max_length
        email_max_length = data._meta.get_field('email').max_length
        ip_max_length = data._meta.get_field('ip').max_length

        self.assertEqual(review_max_length, 500)
        self.assertEqual(name_max_length, 80)
        self.assertEqual(email_max_length, 100)
        self.assertEqual(ip_max_length, 20)

    def test_review_rating_labels(self):
        """Test ReviewRating verbose names"""
        data = self.review_rating

        product = data._meta.get_field('product').verbose_name
        rating = data._meta.get_field('rating').verbose_name
        review = data._meta.get_field('review').verbose_name
        name = data._meta.get_field('name').verbose_name
        email = data._meta.get_field('email').verbose_name
        ip = data._meta.get_field('ip').verbose_name
        created_date = data._meta.get_field('created_date').verbose_name
        modified_date = data._meta.get_field('modified_date').verbose_name
        is_moderated = data._meta.get_field('is_moderated').verbose_name

        self.assertEqual(product, 'товар')
        self.assertEqual(rating, 'рейтинг')
        self.assertEqual(review, 'відгук')
        self.assertEqual(name, "ім'я")
        self.assertEqual(email, 'E-mail')
        self.assertEqual(ip, 'IP адреса')
        self.assertEqual(created_date, 'дата створення')
        self.assertEqual(modified_date, 'дата коригування')
        self.assertEqual(is_moderated, 'промодерований')
