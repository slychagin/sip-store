import datetime
from datetime import date
from importlib import import_module

from django.conf import settings
from django.test import TestCase, Client, RequestFactory

from carts.basket import Basket
from category.models import Category
from orders.models import Order
from store.models import Product
from telebot.models import TelegramSettings
from telebot.telegram import (
    get_telegram_settings,
    send_to_telegram_order_message,
    send_to_telegram_moderate_new_comment_message,
    send_to_telegram_moderate_updated_comment_message,
    send_to_telegram_moderate_new_review_message,
    send_to_telegram_moderate_updated_review_message
)


class TelegramBotTest(TestCase):
    """Tests Telegram Bot settings and functionality"""

    @classmethod
    def setUpTestData(cls):
        """Create telegram settings data, order and basket"""
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create telegram settings in the database
        cls.tg_settings_object = TelegramSettings.objects.create(
            tg_token='token12345',
            tg_chat='123456',
            tg_api='telegram_api_key'
        )
        cls.telegram_method = '/sendMessage'

        # Create Order object
        cls.order_1 = Order.objects.create(
            order_number='2000', customer_name='Сергій', phone='+38(099)777-77-77',
            email='email@gmail.com', city='Черкаси', street='вул. Шевченка', house='7',
            order_total=500, discount=100, delivery_date=date.today(), delivery_time=datetime.time(),
            delivery_method='COURIER_CHERKASY'
        )
        cls.order_2 = Order.objects.create(
            order_number='2000', customer_name='Сергій', phone='+38(099)777-77-77',
            email='email@gmail.com', city='Черкаси', street='вул. Шевченка', house='7',
            order_total=500, discount=100, delivery_date=date.today(), delivery_time=datetime.time(),
            delivery_method='DELIVERY COMPANY'
        )

        # Create products
        category = Category.objects.create(category_name='chicken', slug='chicken')
        cls.product_1 = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='100', product_image='good chicken', category=category
        )
        cls.product_2 = Product.objects.create(
            product_name='super chicken', slug='super-chicken',
            price='200', product_image='good chicken', category=category
        )

    def setUp(self):
        """Add created in setUpTestData products to the basket"""
        self.order_1.communication_method = 'PHONE'
        self.order_1.save()
        self.order_2.communication_method = 'TELEGRAM'
        self.order_2.save()

    def test_telegram_settings(self):
        """Tests telegram settings that get from database"""
        # Return settings if tg_settings_object exists
        tg_settings = get_telegram_settings()
        self.assertIn('chat_id', tg_settings)
        self.assertIn('query', tg_settings)
        self.assertEqual(tg_settings['chat_id'], '123456')
        self.assertEqual(tg_settings['query'], 'telegram_api_keytoken12345/sendMessage')

        # Return IndexError if tg_settings_object not exists
        tg_object = TelegramSettings.objects.get(id=self.tg_settings_object.id)
        tg_object.delete()
        get_telegram_settings()
        self.assertRaises(IndexError)

    def test_send_to_telegram_order_message(self):
        """Tests sending to telegram order message"""
        request = self.factory.get('/cart/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()

        basket = Basket(request)
        basket.add(self.product_1, 1)
        basket.add(self.product_2, 2)

        send_to_telegram_order_message(basket, self.order_1)
        send_to_telegram_order_message(basket, self.order_2)

    def test_send_to_telegram_moderate_new_comment_message(self):
        """Tests sending to telegram moderate new comment message"""
        send_to_telegram_moderate_new_comment_message()

    def test_send_to_telegram_moderate_updated_comment_message(self):
        """Tests sending to telegram moderate updated comment message"""
        send_to_telegram_moderate_updated_comment_message()

    def test_send_to_telegram_moderate_new_review_message(self):
        """Tests sending to telegram moderate new review message"""
        send_to_telegram_moderate_new_review_message()

    def test_send_to_telegram_moderate_updated_review_message(self):
        """Tests sending to telegram moderate updated review message"""
        send_to_telegram_moderate_updated_review_message()
