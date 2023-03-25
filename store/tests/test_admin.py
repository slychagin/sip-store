from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from category.models import Category
from store.admin import ProductGalleryAdmin
from store.models import Product, ProductGallery


class ProductGalleryAdminTest(TestCase):
    """Tests thumbnail format functions in Store admin"""

    @classmethod
    def setUpTestData(cls):
        """Create category, product and product gallery objects"""
        category = Category.objects.create(category_name='pork', slug='pork')
        product = Product.objects.create(
            product_name='chicken', slug='chicken',
            price=100, product_image='good chicken', category_id=category.id
        )

        cls.product_gallery_with_image = ProductGallery.objects.create(
            product=product, image='image'
        )
        cls.product_gallery_without_image = ProductGallery.objects.create(
            product=product
        )

        cls.img_html_tag = '<img src="/media/image" width="40"">'
        cls.img_html_tag_empty = '<img>'

    def test_product_gallery_admin_thumbnail(self):
        """Tests product gallery admin thumbnail"""
        product_gallery_admin = ProductGalleryAdmin(
            model=ProductGallery, admin_site=AdminSite()
        )
        thumbnail_with_image = product_gallery_admin.thumbnail(
            self.product_gallery_with_image
        )
        thumbnail_without_image = product_gallery_admin.thumbnail(
            self.product_gallery_without_image
        )

        self.assertEqual(thumbnail_with_image, self.img_html_tag)
        self.assertEqual(thumbnail_without_image, self.img_html_tag_empty)
