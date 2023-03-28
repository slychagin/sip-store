import json
from datetime import date
from importlib import import_module

from django.conf import settings
from django.test import override_settings
from django.test import (
    TestCase,
    Client,
    RequestFactory
)
from django.urls import reverse

from carts.models import Coupon
from category.models import Category
from orders.forms import OrderForm
from orders.models import (
    OrderItem,
    Customers,
    NewPostTerminals,
    OrderMessage
)
from orders.views import (
    OrderFormView,
    post_city_search,
    post_terminal_search
)
from store.models import Product

from telebot.models import TelegramSettings


class OrderFormViewTest(TestCase):
    """Tests OrderFormView class-based view"""

    @classmethod
    def setUpTestData(cls):
        """Create category and product object"""
        cls.client = Client()
        cls.factory = RequestFactory()
        cls.view = OrderFormView()

        # Create category and products
        category = Category.objects.create(category_name='chicken', slug='chicken')
        cls.product_1 = Product.objects.create(
            product_name='chicken', slug='chicken',
            price=100, product_image='good chicken', category=category
        )
        cls.product_2 = Product.objects.create(
            product_name='pork', slug='pork',
            price=200, product_image='good pork', category=category
        )

        # Create coupon object
        cls.coupon = Coupon.objects.create(
            coupon_kod='AAA', discount=20, validity=date.today()
        )

        # Create telegram settings in the database
        TelegramSettings.objects.create(
            tg_token='token12345',
            tg_chat='123456',
            tg_api='telegram_api_key'
        )

        # Create NewPostTerminal object
        NewPostTerminals.objects.create(city='Boston', terminal='Terminal 1')
        NewPostTerminals.objects.create(city='Boston', terminal='Terminal 2')

        # Create message text for email to customers
        cls.order_message = OrderMessage.objects.create(text_1='Hello!', text_2='Hello!')

    def setUp(self):
        """Add created in setUpTestData products to the basket"""
        self.client.post(
            reverse('add_cart'),
            {'product_id': self.product_1.id, 'quantity': 1, 'action': 'POST'},
            xhr=True
        )
        self.client.post(
            reverse('add_cart'),
            {'product_id': self.product_2.id, 'quantity': 1, 'action': 'POST'},
            xhr=True
        )

        # Create valid form
        self.form = OrderForm(data={
            'order_number': '500',
            'customer_name': 'Sergio',
            'phone': '+38(095)777-77-77',
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
        # Create session engine
        self.engine = import_module(settings.SESSION_ENGINE)

    def test_order_form_view_url_exists_at_desired_location(self):
        """Tests that order form view url exists at desired location"""
        response = self.client.get('/order/')
        self.assertEqual(response.status_code, 200)

    def test_order_form_view_url_accessible_by_name(self):
        """Tests order form view url accessible by name"""
        response = self.client.get(reverse('order_form'))
        self.assertEqual(response.status_code, 200)

    def test_order_form_view_uses_correct_template(self):
        """Tests order form view uses correct template"""
        response = self.client.get(reverse('order_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order.html')

    def test_order_form_view_html(self):
        """Test order form class-based view html"""
        request = self.factory.get('/order/')
        self.view.setup(request)
        response = self.client.get(reverse('order_form'))
        html = response.content.decode('utf8')

        self.assertIn(str(self.product_1), html)
        self.assertIn(str(self.product_2), html)
        self.assertIn('Оформлення замовлення', html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_order_form_view_context(self):
        """Tests order form view context"""
        request = self.factory.get('/order/')
        request.session = self.engine.SessionStore()
        self.view.setup(request)

        # render order page without discount
        response = self.client.get(reverse('order_form'))
        context = response.context

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in context)
        self.assertTrue('basket' in context)
        self.assertTrue('discount' in context)
        self.assertTrue('total_with_discount' in context)
        self.assertTrue(isinstance(context['form'], OrderForm))
        self.assertEqual(context['discount'], 0)
        self.assertEqual(context['total_with_discount'], 300)

        # render order page with discount
        self.client.post(
            reverse('get_coupon'),
            {'coupon': 'aaa', 'action': 'POST'},
            xhr=True
        )
        response = self.client.get(reverse('order_form'))
        context = response.context
        self.assertEqual(context['discount'], 60)
        self.assertEqual(context['total_with_discount'], 240)

    def test_post_method_with_invalid_form(self):
        """
        Tests post method. Check OrderForm. Show form errors.
        """
        # Change the form to make it invalid
        self.form.data['phone'] = ''
        self.form.data['customer_name'] = ''

        # Test with total_price not equal zero
        response = self.client.post(reverse('order_form'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.form.is_valid())
        self.assertFormError(self.form, 'customer_name', "Це поле обов'язкове.")
        self.assertFormError(self.form, 'phone', "Це поле обов'язкове.")

        # Test with total_price equal zero
        # Delete products from the basket
        self.client.post(
            reverse('cart_delete'),
            {'product_id': self.product_1.id, 'action': 'POST'},
            xhr=True
        )
        self.client.post(
            reverse('cart_delete'),
            {'product_id': self.product_2.id, 'action': 'POST'},
            xhr=True
        )
        response = self.client.post(reverse('order_form'))
        self.assertFalse(self.form.is_valid())
        self.assertRedirects(
            response, '/store/', status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_post_method_with_valid_form_with_discount(self):
        """
        Tests post method with valid form.
        """
        # Set discount
        self.client.post(
            reverse('get_coupon'),
            {'coupon': 'aaa', 'action': 'POST'},
            xhr=True
        )

        response = self.client.post(
            reverse('order_form'),
            data=self.form.data
        )

        # Check that form is valid and successful redirect to the thanks page
        self.assertTrue(self.form.is_valid())
        self.assertRedirects(
            response, '/order/thanks/', status_code=302,
            target_status_code=200, fetch_redirect_response=True
        )

        ordered_products = Product.objects.all()

        # Check that was saved product ordered count
        self.assertEqual(ordered_products[0].count_orders, 1)
        self.assertEqual(ordered_products[1].count_orders, 1)

        # Check that was created order items
        ordered_products = OrderItem.objects.all()
        self.assertEqual(len(ordered_products), 2)
        self.assertIn(ordered_products[0], ordered_products)
        self.assertIn(ordered_products[1], ordered_products)

        # Check that customer was saved
        customer = Customers.objects.get(email=self.form.data['email'])
        self.assertTrue(customer)
        self.assertEqual(customer.phone, self.form.data['phone'])

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_post_method_with_valid_form_without_discount(self):
        """
        Tests post method with valid form.
        """
        self.order_message.delete()
        request = self.factory.get('/order/')
        request.session = self.engine.SessionStore()
        self.view.setup(request)

        self.client.post(
            reverse('order_form'),
            data=self.form.data
        )

        with self.assertRaises(KeyError):
            del request.session['discount']

    def test_post_city_search(self):
        """Test post city search function"""

        # If city not in database
        request = self.factory.get('/order/search-city/?term=London')
        response = post_city_search(request)
        decode_response = json.loads(response.content.decode())
        self.assertEqual(decode_response[0], 'Нічого не знайдено')

        # If city in database
        request = self.factory.get('/order/search-city/?term=Boston')
        response = post_city_search(request)
        decode_response = json.loads(response.content.decode())
        self.assertEqual(decode_response[0], 'Boston')

    def test_post_terminal_search_post_method(self):
        """Test post terminal search function if POST method"""
        request = self.factory.post(
            '/order/search-city/',
            {'city_name': 'Boston', 'action': 'POST'}
        )
        request.session = self.engine.SessionStore()
        self.session = request.session

        post_terminal_search(request)

        response = self.client.post(
            reverse('post_terminal_search'),
            {'city_name': 'Boston', 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(response.json(), {'city_name': 'Boston'})
        self.assertEqual(self.session['city'], 'Boston')

    def test_post_terminal_search_get_method(self):
        """Test post terminal search function if GET method"""
        # Try to type city name handle in the search string
        request = self.factory.get('/order/search-city/?term=Boston')
        request.session = self.engine.SessionStore()
        response = post_terminal_search(request)
        decode_response = json.loads(response.content.decode())
        self.assertEqual(decode_response[0], 'Оберіть спочатку місто доставки')

        # If 'term' in search string than try to get city name from session
        request = self.factory.get('/order/search-city/?term')
        request.session = self.engine.SessionStore()
        self.session = request.session

        # If city exist in database
        self.session['city'] = 'Boston'
        response = post_terminal_search(request)
        decode_response = json.loads(response.content.decode())
        self.assertEqual(decode_response, ['Terminal 1', 'Terminal 2'])

        # If city does not exist in database
        self.session['city'] = 'London'
        response = post_terminal_search(request)
        decode_response = json.loads(response.content.decode())
        self.assertEqual(decode_response, ['Нічого не знайдено'])
