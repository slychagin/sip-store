from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from banners.admin import (
    MainBannerAdmin,
    TwoBannersAdmin,
    OfferSingleBannerAdmin,
    FooterBannerAdmin,
    BackgroundBannerAdmin
)
from banners.models import (
    MainBanner,
    TwoBanners,
    OfferSingleBanner,
    FooterBanner,
    BackgroundBanner
)
from category.models import Category
from store.models import Product


class BannersAdminTest(TestCase):
    """Tests thumbnail format functions in Banners admin"""

    @classmethod
    def setUpTestData(cls):
        """Create category, product and banners app objects"""
        category = Category.objects.create(category_name='pork', slug='pork')
        product = Product.objects.create(
            product_name='chicken', slug='chicken',
            price=100, product_image='good chicken', category_id=category.id
        )
        cls.img_html_tag_100 = '<img src="/media/image" width="100"">'
        cls.img_html_tag_120 = '<img src="/media/image" width="120" height="20"">'

        cls.main_banner = MainBanner.objects.create(
            image='image', banner_url=product.get_url()
        )
        cls.two_banners = TwoBanners.objects.create(
            image='image', banner_url=product.get_url()
        )
        cls.offer_single_banner = OfferSingleBanner.objects.create(
            image='image', banner_url=product.get_url()
        )
        cls.footer_banner = FooterBanner.objects.create(
            image='image', banner_url=product.get_url()
        )
        cls.background_banner = BackgroundBanner.objects.create(
            image='image', banner_url=product.get_url()
        )

    def test_main_banner_admin_thumbnail(self):
        """Tests main banner admin thumbnail"""
        main_banner_admin = MainBannerAdmin(model=MainBanner, admin_site=AdminSite())
        thumbnail = main_banner_admin.thumbnail(self.main_banner)
        self.assertEqual(thumbnail, self.img_html_tag_100)

    def test_two_banners_admin_thumbnail(self):
        """Tests two banners admin thumbnail"""
        two_banners_admin = TwoBannersAdmin(model=TwoBanners, admin_site=AdminSite())
        thumbnail = two_banners_admin.thumbnail(self.two_banners)
        self.assertEqual(thumbnail, self.img_html_tag_100)

    def test_offer_single_banner_admin_thumbnail(self):
        """Tests offer single banner admin thumbnail"""
        offer_single_banner_admin = OfferSingleBannerAdmin(model=OfferSingleBanner, admin_site=AdminSite())
        thumbnail = offer_single_banner_admin.thumbnail(self.offer_single_banner)
        self.assertEqual(thumbnail, self.img_html_tag_100)

    def test_footer_banner_admin_thumbnail(self):
        """Tests footer banner admin thumbnail"""
        footer_banner_admin = FooterBannerAdmin(model=FooterBanner, admin_site=AdminSite())
        thumbnail = footer_banner_admin.thumbnail(self.footer_banner)
        self.assertEqual(thumbnail, self.img_html_tag_100)

    def test_background_banner_admin_thumbnail(self):
        """Tests background banner admin thumbnail"""
        background_banner_admin = BackgroundBannerAdmin(model=BackgroundBanner, admin_site=AdminSite())
        thumbnail = background_banner_admin.thumbnail(self.background_banner)
        self.assertEqual(thumbnail, self.img_html_tag_120)
