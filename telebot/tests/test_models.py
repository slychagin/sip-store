from django.test import TestCase

from telebot.models import TelegramSettings


class TelegramSettingsModelTest(TestCase):
    """Tests TelegramSettings model"""

    @classmethod
    def setUpTestData(cls):
        """Create ProductInfo object"""
        cls.telegram_settings = TelegramSettings.objects.create(
            tg_token='bgjdlkjfbfbnf', tg_chat='41215151', tg_api='123.123.12.12'
        )

    def test_telegram_settings_entry(self):
        """Test TelegramSettings model data insertion/types/field attributes"""
        data = self.telegram_settings
        self.assertTrue(isinstance(data, TelegramSettings))

    def test_telegram_settings_model_name(self):
        """Tests TelegramSettings object name"""
        data = self.telegram_settings
        self.assertEqual(str(data), '41215151')

    def test_telegram_settings_max_length(self):
        """Test TelegramSettings fields max length"""
        data = self.telegram_settings

        tg_token_max_length = data._meta.get_field('tg_token').max_length
        tg_chat_max_length = data._meta.get_field('tg_chat').max_length
        tg_api_max_length = data._meta.get_field('tg_api').max_length

        self.assertEqual(tg_token_max_length, 100)
        self.assertEqual(tg_chat_max_length, 100)
        self.assertEqual(tg_api_max_length, 100)

    def test_telegram_settings_labels(self):
        """Test TelegramSettings verbose names"""
        data = self.telegram_settings

        tg_token = data._meta.get_field('tg_token').verbose_name
        tg_chat = data._meta.get_field('tg_chat').verbose_name
        tg_api = data._meta.get_field('tg_api').verbose_name
        tg_message = data._meta.get_field('tg_message').verbose_name
        available = data._meta.get_field('available').verbose_name

        self.assertEqual(tg_token, 'токен')
        self.assertEqual(tg_chat, 'чат ID')
        self.assertEqual(tg_api, 'API адреса')
        self.assertEqual(tg_message, 'текст повідомлення')
        self.assertEqual(available, 'активний')
