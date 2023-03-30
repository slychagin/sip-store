from django.test import TestCase

from banners.models import (
    WeekOfferBanner,
    MainBanner,
    TwoBanners,
    OfferSingleBanner,
    FooterBanner,
    BackgroundBanner
)
from category.models import Category
from store.models import Product


class WeekOfferBannerModelTest(TestCase):
    """Tests the WeekOfferBanner model"""

    @classmethod
    def setUpTestData(cls):
        """Create category, product and WeekOfferBanner objects"""
        category = Category.objects.create(category_name='pork', slug='pork')
        product = Product.objects.create(
            product_name='chicken', slug='chicken',
            price=100, product_image='good chicken', category=category
        )
        cls.week_offer_banner = WeekOfferBanner.objects.create(
            title='banner', product=product, image_active='product_active', image='product'
        )

    def test_week_offer_banner_model_entry(self):
        """
        Test that created week_offer_banner object is
        instance of WeekOfferBanner model banner
        """
        self.assertTrue(isinstance(self.week_offer_banner, WeekOfferBanner))

    def test_week_offer_banner_model_name(self):
        """Tests WeekOfferBanner object name"""
        self.assertEqual(str(self.week_offer_banner), 'banner')

    def test_week_offer_banner_fields_max_length(self):
        """Test WeekOfferBanner fields max length"""
        data = self.week_offer_banner
        title_max_length = data._meta.get_field('title').max_length
        self.assertEqual(title_max_length, 100)

    def test_week_offer_banner_labels(self):
        """Test WeekOfferBanner fields verbose name"""
        data = self.week_offer_banner

        title = data._meta.get_field('title').verbose_name
        product = data._meta.get_field('product').verbose_name
        image_active = data._meta.get_field('image_active').verbose_name
        image = data._meta.get_field('image').verbose_name
        countdown = data._meta.get_field('countdown').verbose_name

        self.assertEqual(title, 'назва банера')
        self.assertEqual(product, 'товар')
        self.assertEqual(image_active, 'фото 1 (активне)')
        self.assertEqual(image, 'фото 2')
        self.assertEqual(countdown, 'таймер')


class MainBannerModelTest(TestCase):
    """Tests MainBanner model"""

    @classmethod
    def setUpTestData(cls):
        """Create MainBanner object"""
        category = Category.objects.create(category_name='pork', slug='pork')
        product = Product.objects.create(
            product_name='chicken', slug='chicken',
            price=100, product_image='good chicken', category=category
        )
        cls.main_banner = MainBanner.objects.create(image='image', banner_url=product.get_url())

    def test_main_banner_model_entry(self):
        """
        Test that created main_banner object is
        instance of MainBanner model banner
        """
        self.assertTrue(isinstance(self.main_banner, MainBanner))

    def test_main_banner_model_name(self):
        """Tests MainBanner object name"""
        self.assertEqual(str(self.main_banner), 'Банер')

    def test_main_banner_fields_max_length(self):
        """Test MainBanner fields max length"""
        data = self.main_banner
        title_max_length = data._meta.get_field('title').max_length
        description_max_length = data._meta.get_field('description').max_length
        banner_url_max_length = data._meta.get_field('banner_url').max_length

        self.assertEqual(title_max_length, 200)
        self.assertEqual(description_max_length, 255)
        self.assertEqual(banner_url_max_length, 255)

    def test_main_banner_labels(self):
        """Test MainBanner fields verbose name"""
        data = self.main_banner

        title = data._meta.get_field('title').verbose_name
        description = data._meta.get_field('description').verbose_name
        image = data._meta.get_field('image').verbose_name
        banner_url = data._meta.get_field('banner_url').verbose_name
        created_date = data._meta.get_field('created_date').verbose_name
        modified_date = data._meta.get_field('modified_date').verbose_name

        self.assertEqual(title, 'заголовок')
        self.assertEqual(description, 'опис')
        self.assertEqual(image, 'фото')
        self.assertEqual(banner_url, 'URL банера')
        self.assertEqual(created_date, 'дата створення')
        self.assertEqual(modified_date, 'дата коригування')


class TwoBannersModelTest(TestCase):
    """Tests TwoBanners model"""

    @classmethod
    def setUpTestData(cls):
        """Create TwoBanners object"""
        category = Category.objects.create(category_name='pork', slug='pork')
        product = Product.objects.create(
            product_name='chicken', slug='chicken',
            price=100, product_image='good chicken', category=category
        )
        cls.two_banners = TwoBanners.objects.create(
            title='SuperBanner', image='image', banner_url=product.get_url()
        )

    def test_two_banners_model_entry(self):
        """
        Test that created two_banner object is
        instance of TwoBanners model banner
        """
        self.assertTrue(isinstance(self.two_banners, TwoBanners))

    def test_two_banners_model_name(self):
        """Tests TwoBanners object name"""
        self.assertEqual(str(self.two_banners), 'SuperBanner')

    def test_two_banners_fields_max_length(self):
        """Test TwoBanners fields max length"""
        data = self.two_banners
        title_max_length = data._meta.get_field('title').max_length
        banner_url_max_length = data._meta.get_field('banner_url').max_length

        self.assertEqual(title_max_length, 100)
        self.assertEqual(banner_url_max_length, 255)

    def test_two_banners_labels(self):
        """Test TwoBanners fields verbose name"""
        data = self.two_banners

        title = data._meta.get_field('title').verbose_name
        image = data._meta.get_field('image').verbose_name
        banner_url = data._meta.get_field('banner_url').verbose_name

        self.assertEqual(title, 'заголовок')
        self.assertEqual(image, 'фото')
        self.assertEqual(banner_url, 'URL банера')


class OfferSingleBannerModelTest(TestCase):
    """Tests OfferSingleBanner model"""

    @classmethod
    def setUpTestData(cls):
        """Create OfferSingleBanner object"""
        category = Category.objects.create(category_name='pork', slug='pork')
        product = Product.objects.create(
            product_name='chicken', slug='chicken',
            price=100, product_image='good chicken', category=category
        )
        cls.offer_single_banner = OfferSingleBanner.objects.create(
            image='image', banner_url=product.get_url()
        )

    def test_offer_single_banner_model_entry(self):
        """
        Test that created offer_single_banner object is
        instance of OfferSingleBanner model banner
        """
        self.assertTrue(isinstance(self.offer_single_banner, OfferSingleBanner))

    def test_offer_single_banner_model_name(self):
        """Tests OfferSingleBanner object name"""
        self.assertEqual(str(self.offer_single_banner), 'Одиночний банер зліва')

    def test_offer_single_banner_fields_max_length(self):
        """Test OfferSingleBanner fields max length"""
        data = self.offer_single_banner
        banner_url_max_length = data._meta.get_field('banner_url').max_length

        self.assertEqual(banner_url_max_length, 255)

    def test_offer_single_banner_labels(self):
        """Test OfferSingleBanner fields verbose name"""
        data = self.offer_single_banner

        image = data._meta.get_field('image').verbose_name
        banner_url = data._meta.get_field('banner_url').verbose_name

        self.assertEqual(image, 'фото')
        self.assertEqual(banner_url, 'URL банера')


class FooterBannerModelTest(TestCase):
    """Tests OfferSingleBanner model"""

    @classmethod
    def setUpTestData(cls):
        """Create FooterBanner object"""
        category = Category.objects.create(category_name='pork', slug='pork')
        product = Product.objects.create(
            product_name='chicken', slug='chicken',
            price=100, product_image='good chicken', category=category
        )
        cls.footer_banner = FooterBanner.objects.create(
            image='image', banner_url=product.get_url()
        )

    def test_footer_banner_model_entry(self):
        """
        Test that created footer_banner object is
        instance of FooterBanner model banner
        """
        self.assertTrue(isinstance(self.footer_banner, FooterBanner))

    def test_footer_banner_model_name(self):
        """Tests FooterBanner object name"""
        self.assertEqual(str(self.footer_banner), 'Футер банер')

    def test_footer_banner_fields_max_length(self):
        """Test FooterBanner fields max length"""
        data = self.footer_banner
        banner_url_max_length = data._meta.get_field('banner_url').max_length

        self.assertEqual(banner_url_max_length, 255)

    def test_footer_banner_labels(self):
        """Test FooterBanner fields verbose name"""
        data = self.footer_banner

        image = data._meta.get_field('image').verbose_name
        banner_url = data._meta.get_field('banner_url').verbose_name

        self.assertEqual(image, 'фото')
        self.assertEqual(banner_url, 'URL банера')


class BackgroundBannerModelTest(TestCase):
    """Tests BackgroundBanner model"""

    @classmethod
    def setUpTestData(cls):
        """Create BackgroundBanner object"""
        category = Category.objects.create(category_name='pork', slug='pork')
        product = Product.objects.create(
            product_name='chicken', slug='chicken',
            price=100, product_image='good chicken', category=category
        )
        cls.background_banner = BackgroundBanner.objects.create(
            image='image', banner_url=product.get_url()
        )

    def test_background_banner_model_entry(self):
        """
        Test that created background_banner object is
        instance of BackgroundBanner model banner
        """
        self.assertTrue(isinstance(self.background_banner, BackgroundBanner))

    def test_background_banner_model_name(self):
        """Tests BackgroundBanner object name"""
        self.assertEqual(str(self.background_banner), 'Фоновий банер')

    def test_background_banner_fields_max_length(self):
        """Test BackgroundBanner fields max length"""
        data = self.background_banner
        banner_url_max_length = data._meta.get_field('banner_url').max_length

        self.assertEqual(banner_url_max_length, 255)

    def test_background_banner_labels(self):
        """Test BackgroundBanner fields verbose name"""
        data = self.background_banner

        image = data._meta.get_field('image').verbose_name
        banner_url = data._meta.get_field('banner_url').verbose_name

        self.assertEqual(image, 'фото')
        self.assertEqual(banner_url, 'URL банера')
