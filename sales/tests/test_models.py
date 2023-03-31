from django.test import TestCase

from category.models import Category
from sales.models import (
    BestSellers,
    BlockTitle,
    MostPopularCenter,
    MostPopularLeft,
    MostPopularRight,
    NewProducts,
)
from store.models import Product


class BlockTitleModelTest(TestCase):
    """Tests BlockTitle model"""

    @classmethod
    def setUpTestData(cls):
        cls.block_title = BlockTitle.objects.create(title='bestsellers')

    def test_block_title_model_entry(self):
        """
        Test that created BlockTitle object is
        instance of BlockTitle model
        """
        self.assertTrue(isinstance(self.block_title, BlockTitle))

    def test_block_title_model_name(self):
        """Tests BlockTitle name"""
        self.assertEqual(str(self.block_title), 'bestsellers')

    def test_block_title_label(self):
        """Test BlockTitle title verbose name"""
        field_label = self.block_title._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'назва блоку')

    def test_block_title_max_length(self):
        """Test BlockTitle title max length"""
        max_length = self.block_title._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)


class BestSellersModelTest(TestCase):
    """Tests BestSellers model"""

    @classmethod
    def setUpTestData(cls):
        """Create BestSellers object"""
        category = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(2):
            Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price=120, product_image='good chicken', category=category
            )
        products = Product.objects.all()

        block_title = BlockTitle.objects.create(title='bestsellers')
        cls.best_seller = BestSellers.objects.create(
            title=block_title, product_1=products[0],
            image_prod1_active='image1_active', image_prod1='image1',
            product_2=products[1], image_prod2_active='image2_active',
            image_prod2='image2'
        )

    def test_bestsellers_model_entry(self):
        """
        Test that created BestSellers object is
        instance of BestSellers model
        """
        self.assertTrue(isinstance(self.best_seller, BestSellers))

    def test_bestsellers_model_name(self):
        """Tests BestSellers name"""
        self.assertEqual(
            str(self.best_seller), f'Секція: {self.best_seller.product_1}, {self.best_seller.product_2}'
        )


class NewProductsModelTest(TestCase):
    """Tests NewProducts model"""

    @classmethod
    def setUpTestData(cls):
        """Create NewProducts object"""
        category = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(2):
            Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price=120, product_image='good chicken', category=category
            )
        products = Product.objects.all()

        block_title = BlockTitle.objects.create(title='new products')
        cls.new_product = NewProducts.objects.create(
            title=block_title, product_1=products[0], image_prod1_active='image1_active',
            image_prod1='image1', product_2=products[1], image_prod2_active='image2_active', image_prod2='image2'
        )

    def test_new_products_model_entry(self):
        """
        Test that created NewProducts object is
        instance of NewProducts model
        """
        self.assertTrue(isinstance(self.new_product, NewProducts))

    def test_new_products_model_name(self):
        """Tests NewProducts name"""
        self.assertEqual(
            str(self.new_product), f'Секція: {self.new_product.product_1}, {self.new_product.product_2}'
        )


class MostPopularLeftModelTest(TestCase):
    """Tests MostPopularLeft model"""

    @classmethod
    def setUpTestData(cls):
        """Create MostPopularLeft object"""
        category = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(3):
            Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price=120, product_image='good chicken', category=category
            )
        products = Product.objects.all()

        block_title = BlockTitle.objects.create(title='most popular products')
        cls.most_popular_left = MostPopularLeft.objects.create(
            title=block_title, product_1=products[0], image_prod1_active='image1_active',
            image_prod1='image1', product_2=products[1], image_prod2_active='image2_active', image_prod2='image2',
            product_3=products[2], image_prod3_active='image3_active', image_prod3='image3'
        )

    def test_most_popular_left_model_entry(self):
        """
        Test that created MostPopularLeft object is
        instance of MostPopularLeft model
        """
        self.assertTrue(isinstance(self.most_popular_left, MostPopularLeft))

    def test_most_popular_left_model_name(self):
        """Tests MostPopularLeft name"""
        self.assertEqual(
            str(self.most_popular_left),
            f'Секція: '
            f'{self.most_popular_left.product_1}, '
            f'{self.most_popular_left.product_2}, '
            f'{self.most_popular_left.product_3}'
        )


class MostPopularCenterModelTest(TestCase):
    """Tests MostPopularCenter model"""

    @classmethod
    def setUpTestData(cls):
        """Create MostPopularCenter object"""
        category = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(3):
            Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price=120, product_image='good chicken', category=category
            )
        products = Product.objects.all()

        block_title = BlockTitle.objects.create(title='most popular products')
        cls.most_popular_center = MostPopularCenter.objects.create(
            title=block_title, product_1=products[0], image_prod1_active='image1_active',
            image_prod1='image1', product_2=products[1], image_prod2_active='image2_active', image_prod2='image2',
            product_3=products[2], image_prod3_active='image3_active', image_prod3='image3'
        )

    def test_most_popular_center_model_entry(self):
        """
        Test that created MostPopularCenter object is
        instance of MostPopularCenter model
        """
        self.assertTrue(isinstance(self.most_popular_center, MostPopularCenter))

    def test_most_popular_center_model_name(self):
        """Tests MostPopularCenter name"""
        self.assertEqual(
            str(self.most_popular_center),
            f'Секція: '
            f'{self.most_popular_center.product_1}, '
            f'{self.most_popular_center.product_2}, '
            f'{self.most_popular_center.product_3}'
        )


class MostPopularRightModelTest(TestCase):
    """Tests MostPopularRight model"""

    @classmethod
    def setUpTestData(cls):
        """Create MostPopularRight object"""
        category = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(3):
            Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price=120, product_image='good chicken', category=category
            )
        products = Product.objects.all()

        block_title = BlockTitle.objects.create(title='most popular products')
        cls.most_popular_right = MostPopularRight.objects.create(
            title=block_title, product_1=products[0], image_prod1_active='image1_active',
            image_prod1='image1', product_2=products[1], image_prod2_active='image2_active', image_prod2='image2',
            product_3=products[2], image_prod3_active='image3_active', image_prod3='image3'
        )

    def test_most_popular_right_model_entry(self):
        """
        Test that created MostPopularRight object is
        instance of MostPopularRight model
        """
        self.assertTrue(isinstance(self.most_popular_right, MostPopularRight))

    def test_most_popular_right_model_name(self):
        """Tests MostPopularRight name"""
        self.assertEqual(
            str(self.most_popular_right),
            f'Секція: {self.most_popular_right.product_1}, '
            f'{self.most_popular_right.product_2}, '
            f'{self.most_popular_right.product_3}'
        )
