from importlib import import_module
from urllib.parse import urlencode

from django.conf import settings
from django.test import (
    TestCase,
    Client,
    RequestFactory
)
from django.urls import reverse

from category.models import Category
from orders.models import Order, OrderItem
from store.forms import ProductsSortForm
from store.models import Product, ReviewRating
from store.views import (
    StorePageView,
    ProductsByCategoryListView,
    ProductDetailView, SearchListView
)
from telebot.models import TelegramSettings


class StorePageViewTest(TestCase):
    """Tests StorePageView"""

    def setUp(self):
        """Create category and product object"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = StorePageView()

        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=120, product_image='good chicken', category=self.category
        )
        self.product_1 = Product.objects.create(
            product_name='fitness pork', slug='fitness-pork',
            price=100, product_image='good pork', category=self.category
        )

        # Create rating for products for test rating ordering
        ReviewRating.objects.create(
            product=self.product, rating=2.0, review='Good product!',
            name='Serhio', email='gmail@gmail.com', is_moderated=True
        )
        ReviewRating.objects.create(
            product=self.product_1, rating=5.0, review='Bad product!',
            name='Serhio', email='gmail@gmail.com', is_moderated=True
        )

    def test_store_page_view_url_exists_at_desired_location(self):
        """Tests that store view url exists at desired location"""
        response = self.client.get('/store/')
        self.assertEqual(response.status_code, 200)

    def test_store_page_view_url_accessible_by_name(self):
        """Tests store view url accessible by name"""
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)

    def test_store_page_view_uses_correct_template(self):
        """Tests store view uses correct template"""
        response = self.client.get(reverse('store'))
        self.assertTemplateUsed(response, 'store/store.html')

    def test_store_page_html(self):
        """Test StorePage html"""
        request = self.factory.get('/store/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf-8')

        self.assertIn(str(self.category), html)
        self.assertIn(str(self.product), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_store_page_view_context(self):
        """Tests StorePageView context"""
        request = self.factory.get('/store/')
        self.view.setup(request)
        context = self.view.get_context_data()

        self.assertTrue(len(context['products']) == 2)
        self.assertTrue(context['product_count'] == 2)
        self.assertTrue(isinstance(context['form'], ProductsSortForm))

    def test_rating_ordering(self):
        """Tests rating ordering in StorePageView"""
        request = self.factory.get('/store/?ordering=rating')
        self.view.setup(request)
        self.view.get_queryset()
        sorted_product_list = self.view.get_queryset()

        self.assertEqual(sorted_product_list[0], self.product_1)
        self.assertEqual(sorted_product_list[1], self.product)


class ProductsByCategoryListViewTest(TestCase):
    """Tests ProductsByCategoryListView class-based view"""

    def setUp(self):
        """Create category and product object"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = ProductsByCategoryListView()
        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=120, product_image='good chicken', category=self.category
        )

    def test_products_by_category_list_view_url_exists_at_desired_location(self):
        """Tests that products by category view url exists at desired location"""
        response = self.client.get('/store/category/chicken/')
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_list_view_url_accessible_by_name(self):
        """Tests products by category view url accessible by name"""
        response = self.client.get(reverse('products_by_category', args=['chicken']))
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_list_view_uses_correct_template(self):
        """Tests product by category view uses correct template"""
        response = self.client.get(reverse('products_by_category', args=['chicken']))
        self.assertTemplateUsed(response, 'store/store.html')

    def test_products_by_category_list_view(self):
        """Test product by category view"""
        request = self.factory.get('/store/chicken/')
        self.view.setup(request)
        response = self.client.get(reverse('products_by_category', args=['chicken']))
        html = response.content.decode('utf8')

        self.assertIn(str(self.category), html)
        self.assertIn(str(self.product), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_products_by_category_list_view_context(self):
        """Tests product by category view context"""
        response = self.client.get(reverse('products_by_category', args=['chicken']))
        context = response.context

        self.assertTrue(len(context['products']) == 1)
        self.assertTrue(context['product_count'] == 1)
        self.assertEqual(response.status_code, 200)


class ProductDetailViewTest(TestCase):
    """Tests ProductDetailView class-based view"""

    def setUp(self):
        """Create category and product object"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = ProductDetailView()

        # Create category and product
        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=120, product_image='good chicken', category=self.category
        )

        # Create order and order item (this need for check review form)
        self.order = Order.objects.create(
            order_number='3000', customer_name='Sergio', phone='+38(099)777-77-77',
            email='email@gmail.com', city='Черкаси', street='вул. Шевченка', house='7',
            order_total=120, discount=0
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, price=self.product.price, user_email=self.order.email
        )

        # Create telegram settings in the database
        TelegramSettings.objects.create(
            tg_token='token12345',
            tg_chat='123456',
            tg_api='telegram_api_key'
        )

    def test_product_detail_view_url_exists_at_desired_location(self):
        """Tests that product detail view url exists at desired location"""
        response = self.client.get('/store/category/chicken/fitness-chicken/')
        self.assertEqual(response.status_code, 200)

    def test_product_details_view_url_accessible_by_name(self):
        """Tests product details view url accessible by name"""
        response = self.client.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        self.assertEqual(response.status_code, 200)

    def test_product_details_view_uses_correct_template(self):
        """Tests product details view uses correct template"""
        response = self.client.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_details.html')

    def test_product_detail_view(self):
        """Test product detail class-based view"""
        request = self.factory.get('/store/chicken/fitness-chicken/')
        self.view.setup(request)
        response = self.client.get(reverse('product_details', args=['chicken', 'fitness-chicken']))
        html = response.content.decode('utf8')

        self.assertIn(str(self.category), html)
        self.assertIn(str(self.product), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_context(self):
        """Tests product detail view context"""
        response = self.client.get(
            reverse('product_details', args=['chicken', 'fitness-chicken'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('single_product' in response.context)
        self.assertEqual(response.context['single_product'].product_name, 'fitness chicken')

    def test_product_detail_404_page(self):
        """Test render 404 page if requested product does not exists"""
        request = self.factory.get('/store/not-found/not-found/')
        self.view.setup(request)
        response = self.client.get(reverse('product_details', args=['chicken', 'fitness-chicken-not-found']))
        self.assertEqual(response.status_code, 404)

    def test_product_detail_view_post_method_with_invalid_form(self):
        """
        Tests post method. Check ReviewRatingForm. Show form errors.
        """
        data = {
            'rating': 0,
            'review': 'This is a good product',
            'name': 'Sergio',
            'email': '',
        }

        response = self.client.post(
            reverse('product_details', args=[self.category.slug, self.product.slug]),
            data=urlencode(data),
            xhr=True,
            content_type='application/x-www-form-urlencoded',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertFormError(response, 'form', 'email', "Це поле обов'язкове.")

    def test_post_method_with_valid_form_not_ordered_product(self):
        """
        Tests post method. Check ReviewRatingForm. If the user did
        not buy the product, a message is displayed that in order
        to leave a review it is necessary to buy this product
        """
        data = {
            'rating': 5.0,
            'review': 'This is a good product',
            'name': 'Sergio',
            'email': 'sergio@example.com',
        }

        response = self.client.post(
            reverse('product_details', args=[self.category.slug, self.product.slug]),
            data=urlencode(data),
            xhr=True,
            content_type='application/x-www-form-urlencoded',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'info': True})

    def test_post_method_with_valid_form_product_ordered_new_review(self):
        """
        Tests post method. Check ReviewRatingForm. If the user
        buy the product and not leave review than create and
        save in the database new review
        """
        data = {
            'rating': 5.0,
            'review': 'This is a good product',
            'name': 'Sergio',
            'email': 'email@gmail.com',
        }

        response = self.client.post(
            reverse('product_details', args=[self.category.slug, self.product.slug]),
            data=urlencode(data),
            xhr=True,
            content_type='application/x-www-form-urlencoded',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        review = ReviewRating.objects.get(product=self.product, email=self.order.email)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        self.assertTrue(review)

    def test_post_method_with_valid_form_product_ordered_update_review(self):
        """
        Tests post method. Check ReviewRatingForm. If the user
        buy the product and leave review than update review.
        """
        data = {
            'rating': 5.0,
            'review': 'This is a good product',
            'name': 'Sergio',
            'email': 'email@gmail.com',
        }

        # Create a review to emulate the review update script
        ReviewRating.objects.create(
            product=self.product, rating=3.5, review='A good product!',
            name='Sergio', email='email@gmail.com'
        )

        response = self.client.post(
            reverse('product_details', args=[self.category.slug, self.product.slug]),
            data=urlencode(data),
            xhr=True,
            content_type='application/x-www-form-urlencoded',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        reviews = ReviewRating.objects.filter(product=self.product, email=self.order.email)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'update': True})
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0].rating, 5.0)
        self.assertEqual(reviews[0].review, 'This is a good product')
        self.assertEqual(reviews[0].name, 'Sergio')
        self.assertEqual(reviews[0].email, 'email@gmail.com')


class SearchListViewTest(TestCase):
    """Tests SearchListView"""

    @classmethod
    def setUpTestData(cls):
        """Create client, category and product object"""
        cls.client = Client()
        cls.factory = RequestFactory()
        cls.view = SearchListView()

        cls.category = Category.objects.create(category_name='chicken', slug='chicken')
        category_id = Category.objects.get(category_name='chicken').id
        cls.product_1 = Product.objects.create(
            product_name='awsome chicken', slug='fitness-chicken', description='good and testy',
            price=100, product_image='fitness chicken', category_id=category_id
        )
        cls.product_2 = Product.objects.create(
            product_name='awsome pork', slug='pork', description='good fresh',
            price=200, product_image='good pork', category_id=category_id
        )
        cls.product_3 = Product.objects.create(
            product_name='awsome ham', slug='ham', description='good new',
            price=300, product_image='good ham', category_id=category_id
        )

    def test_search_list_view_url_exists_at_desired_location(self):
        """Tests that search list view url exists at desired location"""
        response = self.client.get('/store/search/')
        self.assertEqual(response.status_code, 200)

    def test_search_list_view_url_accessible_by_name(self):
        """Tests search list view url accessible by name"""
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    def test_search_list_view_uses_correct_template(self):
        """Tests search list view uses correct template"""
        response = self.client.get(reverse('search'))
        self.assertTemplateUsed(response, 'store/store.html')

    def test_search_list_view_html(self):
        """Test SearchListView html"""
        request = self.factory.get('/store/search/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf-8')

        self.assertIn(str(self.category), html)
        self.assertIn(str(self.product_1), html)
        self.assertIn(str(self.product_2), html)
        self.assertIn(str(self.product_3), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_context_with_empty_search_string(self):
        """Tests SearchListView context with empty search string"""
        request = self.factory.get('/store/search/')
        self.view.setup(request)
        context = self.view.get_context_data()

        self.assertEqual(context['product_count'], 0)
        self.assertTrue(context['products'] is None)

    def test_context_with_unique_product_name_in_search_string(self):
        """
        Tests SearchListView context with unique word in product name
        that was entered in search string
        """
        request = self.factory.get('/store/search/?keyword=chicken')
        self.view.setup(request)
        self.view.get_queryset()
        context = self.view.get_context_data()

        self.assertEqual(context['product_count'], 1)
        self.assertIn(self.product_1, context['products'])

    def test_context_with_unique_description_in_search_string(self):
        """
        Tests SearchListView context with unique description
        in product name that was entered in search string
        """
        request = self.factory.get('/store/search/?keyword=fresh')
        self.view.setup(request)
        self.view.get_queryset()
        context = self.view.get_context_data()

        self.assertEqual(context['product_count'], 1)
        self.assertIn(self.product_2, context['products'])

    def test_context_with_recurring_product_name_in_search_string(self):
        """
        Tests SearchListView context with recurring word in product name
        that was entered in search string
        """
        request = self.factory.get('/store/search/?keyword=awsome')
        self.view.setup(request)
        self.view.get_queryset()
        context = self.view.get_context_data()

        self.assertEqual(context['product_count'], 3)
        self.assertIn(self.product_1, context['products'])
        self.assertIn(self.product_2, context['products'])
        self.assertIn(self.product_3, context['products'])

    def test_context_with_recurring_description_in_search_string(self):
        """
        Tests SearchListView context with recurring description
        in product name that was entered in search string
        """
        request = self.factory.get('/store/search/?keyword=good')
        self.view.setup(request)
        self.view.get_queryset()
        context = self.view.get_context_data()

        self.assertEqual(context['product_count'], 3)
        self.assertIn(self.product_1, context['products'])
        self.assertIn(self.product_2, context['products'])
        self.assertIn(self.product_3, context['products'])


class LoadMoreReviewsTest(TestCase):
    """Tests load more reviews function"""

    def setUp(self):
        """Create category, products and reviews objects"""
        self.client = Client()
        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price=100, product_image='good chicken', category=self.category
        )

        # Create 12 reviews for product (3 reviews are shown immediately
        # when the page is loaded and then, by pressing a button,
        # it shows 10 reviews each)
        for i in range(20):
            ReviewRating.objects.create(
                product=self.product, rating=5.0, review='A good product!',
                name='Sergio', email=f'mail{i}@gmail.com', is_moderated=True
            )

    def test_load_more_reviews(self):
        """Test load more reviews function"""
        # After the page loads, three reviews are displayed. Hidden 17 reviews.
        # Press button "show more reviews" (show next 10 reviews, left 7 reviews)
        response = self.client.post(
            reverse('load_more_reviews'),
            {'product_id': self.product.id, 'visible_reviews': 10, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(len(response.json()['data']), 10)

        # Press button "show more reviews" one more (show next 7 reviews, left 0 reviews)
        response = self.client.post(
            reverse('load_more_reviews'),
            {'product_id': self.product.id, 'visible_reviews': 20, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(len(response.json()['data']), 7)











