from django.test import TestCase

from banners.models import WeekOfferBanner
from category.models import Category
from store.models import Product


class WeekOfferBannerModelTest(TestCase):
    """Tests WeekOfferBanner model"""

    def setUp(self):
        """Create WeekOfferBanner object"""
        self.category = Category.objects.create(category_name='chicken', slug='chicken')
        self.product = Product.objects.create(
            product_name='fitness chicken', slug='fitness-chicken',
            price='120', product_image='good chicken', category_id=1
        )
        self.banner = WeekOfferBanner.objects.create(
            title='banner', product_id=1, image_active='product_active', image='product'
        )

    def test_week_offer_banner_model_entry(self):
        """Test WeekOfferBanner model data insertion/types/field attributes"""
        data = self.banner
        self.assertTrue(isinstance(data, WeekOfferBanner))

    def test_week_offer_banner_model_name(self):
        """Tests WeekOfferBanner name"""
        data = self.banner
        self.assertEqual(str(data), 'banner')

    def test_week_offer_banner_title_label(self):
        """Test WeekOfferBanner title verbose name"""
        data = self.banner
        field_label = data._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Назва банера')

    def test_week_offer_banner_product_label(self):
        """Test WeekOfferBanner product verbose name"""
        data = self.banner
        field_label = data._meta.get_field('product').verbose_name
        self.assertEqual(field_label, 'Товар')

    def test_week_offer_banner_image_active_label(self):
        """Test WeekOfferBanner image active verbose name"""
        data = self.banner
        field_label = data._meta.get_field('image_active').verbose_name
        self.assertEqual(field_label, 'Фото 1 (активне)')

    def test_week_offer_banner_image_label(self):
        """Test WeekOfferBanner image verbose name"""
        data = self.banner
        field_label = data._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'Фото 2')

    def test_week_offer_banner_title_max_length(self):
        """Test WeekOfferBanner title max length"""
        data = self.banner
        max_length = data._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)
