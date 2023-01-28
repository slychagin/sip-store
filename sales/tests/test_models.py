from django.test import TestCase

from category.models import Category
from store.models import Product
from sales.models import (
    BlockTitle,
    BestSellers,
    NewProducts,
    MostPopularLeft,
    MostPopularCenter,
    MostPopularRight
)


class BlockTitleModelTest(TestCase):
    """Tests BlockTitle model"""

    def setUp(self):
        self.block_title_data = BlockTitle.objects.create(title='bestsellers')

    def test_block_title_model_entry(self):
        """Test BlockTitle model data insertion/types/field attributes"""
        data = self.block_title_data
        self.assertTrue(isinstance(data, BlockTitle))

    def test_block_title_model_name(self):
        """Tests BlockTitle name"""
        data = self.block_title_data
        self.assertEqual(str(data), 'bestsellers')

    def test_block_title_label(self):
        """Test BlockTitle title verbose name"""
        data = self.block_title_data
        field_label = data._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Назва блоку')

    def test_block_title_max_length(self):
        """Test BlockTitle title max length"""
        data = self.block_title_data
        max_length = data._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)


class BestSellersModelTest(TestCase):
    """Tests BestSellers model"""

    def setUp(self):
        """Create BestSellers object"""
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(2):
            self.product_data = Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price='120', product_image='good chicken', category_id=1
            )

        self.block_title_data = BlockTitle.objects.create(title='bestsellers')
        self.best_sellers_data = BestSellers.objects.create(
            title_id=1, product_1_id=1, image_prod1_active='image1_active',
            image_prod1='image1', product_2_id=2, image_prod2_active='image2_active', image_prod2='image2'
        )

    def test_bestsellers_model_entry(self):
        """Test BestSellers model data insertion/types/field attributes"""
        data = self.best_sellers_data
        self.assertTrue(isinstance(data, BestSellers))

    def test_bestsellers_model_name(self):
        """Tests BestSellers name"""
        data = self.best_sellers_data
        self.assertEqual(str(data), 'Секція: fitness chicken0, fitness chicken1')


class NewProductsModelTest(TestCase):
    """Tests NewProducts model"""

    def setUp(self):
        """Create NewProducts object"""
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(2):
            self.product_data = Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price='120', product_image='good chicken', category_id=1
            )

        self.block_title_data = BlockTitle.objects.create(title='new products')
        self.new_products_data = NewProducts.objects.create(
            title_id=1, product_1_id=1, image_prod1_active='image1_active',
            image_prod1='image1', product_2_id=2, image_prod2_active='image2_active', image_prod2='image2'
        )

    def test_new_products_model_entry(self):
        """Test NewProducts model data insertion/types/field attributes"""
        data = self.new_products_data
        self.assertTrue(isinstance(data, NewProducts))

    def test_new_products_model_name(self):
        """Tests NewProducts name"""
        data = self.new_products_data
        self.assertEqual(str(data), 'Секція: fitness chicken0, fitness chicken1')


class MostPopularLeftModelTest(TestCase):
    """Tests MostPopularLeft model"""

    def setUp(self):
        """Create MostPopularLeft object"""
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(3):
            self.product_data = Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price='120', product_image='good chicken', category_id=1
            )

        self.block_title_data = BlockTitle.objects.create(title='most popular products')
        self.most_popular_products_data = MostPopularLeft.objects.create(
            title_id=1, product_1_id=1, image_prod1_active='image1_active',
            image_prod1='image1', product_2_id=2, image_prod2_active='image2_active', image_prod2='image2',
            product_3_id=3, image_prod3_active='image3_active', image_prod3='image3'
        )

    def test_most_popular_left_model_entry(self):
        """Test MostPopularLeft model data insertion/types/field attributes"""
        data = self.most_popular_products_data
        self.assertTrue(isinstance(data, MostPopularLeft))

    def test_most_popular_left_model_name(self):
        """Tests MostPopularLeft name"""
        data = self.most_popular_products_data
        self.assertEqual(
            str(data), 'Секція: fitness chicken0, fitness chicken1, fitness chicken2'
        )


class MostPopularCenterModelTest(TestCase):
    """Tests MostPopularCenter model"""

    def setUp(self):
        """Create MostPopularCenter object"""
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(3):
            self.product_data = Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price='120', product_image='good chicken', category_id=1
            )

        self.block_title_data = BlockTitle.objects.create(title='most popular products')
        self.most_popular_products_data = MostPopularCenter.objects.create(
            title_id=1, product_1_id=1, image_prod1_active='image1_active',
            image_prod1='image1', product_2_id=2, image_prod2_active='image2_active', image_prod2='image2',
            product_3_id=3, image_prod3_active='image3_active', image_prod3='image3'
        )

    def test_most_popular_center_model_entry(self):
        """Test MostPopularCenter model data insertion/types/field attributes"""
        data = self.most_popular_products_data
        self.assertTrue(isinstance(data, MostPopularCenter))

    def test_most_popular_center_model_name(self):
        """Tests MostPopularCenter name"""
        data = self.most_popular_products_data
        self.assertEqual(
            str(data), 'Секція: fitness chicken0, fitness chicken1, fitness chicken2'
        )


class MostPopularRightModelTest(TestCase):
    """Tests MostPopularRight model"""

    def setUp(self):
        """Create MostPopularRight object"""
        self.category_data = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(3):
            self.product_data = Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price='120', product_image='good chicken', category_id=1
            )

        self.block_title_data = BlockTitle.objects.create(title='most popular products')
        self.most_popular_products_data = MostPopularRight.objects.create(
            title_id=1, product_1_id=1, image_prod1_active='image1_active',
            image_prod1='image1', product_2_id=2, image_prod2_active='image2_active', image_prod2='image2',
            product_3_id=3, image_prod3_active='image3_active', image_prod3='image3'
        )

    def test_most_popular_right_model_entry(self):
        """Test MostPopularRight model data insertion/types/field attributes"""
        data = self.most_popular_products_data
        self.assertTrue(isinstance(data, MostPopularRight))

    def test_most_popular_right_model_name(self):
        """Tests MostPopularRight name"""
        data = self.most_popular_products_data
        self.assertEqual(
            str(data), 'Секція: fitness chicken0, fitness chicken1, fitness chicken2'
        )
