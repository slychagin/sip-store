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

    @classmethod
    def setUpTestData(cls):
        cls.block_title = BlockTitle.objects.create(title='bestsellers')

    def test_block_title_model_entry(self):
        """Test BlockTitle model data insertion/types/field attributes"""
        data = self.block_title
        self.assertTrue(isinstance(data, BlockTitle))

    def test_block_title_model_name(self):
        """Tests BlockTitle name"""
        data = self.block_title
        self.assertEqual(str(data), 'bestsellers')

    def test_block_title_label(self):
        """Test BlockTitle title verbose name"""
        data = self.block_title
        field_label = data._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'назва блоку')

    def test_block_title_max_length(self):
        """Test BlockTitle title max length"""
        data = self.block_title
        max_length = data._meta.get_field('title').max_length
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
                price=120, product_image='good chicken', category_id=category.id
            )
        products = Product.objects.all()

        block_title = BlockTitle.objects.create(title='bestsellers')
        cls.best_seller = BestSellers.objects.create(
            title_id=block_title.id, product_1_id=products[0].id,
            image_prod1_active='image1_active', image_prod1='image1',
            product_2_id=products[1].id, image_prod2_active='image2_active',
            image_prod2='image2'
        )

    def test_bestsellers_model_entry(self):
        """Test BestSellers model data insertion/types/field attributes"""
        data = self.best_seller
        self.assertTrue(isinstance(data, BestSellers))

    def test_bestsellers_model_name(self):
        """Tests BestSellers name"""
        data = self.best_seller
        self.assertEqual(str(data), f'Секція: {self.best_seller.product_1}, {self.best_seller.product_2}')


class NewProductsModelTest(TestCase):
    """Tests NewProducts model"""

    @classmethod
    def setUpTestData(cls):
        """Create NewProducts object"""
        category = Category.objects.create(category_name='chicken', slug='chicken')

        for n in range(2):
            Product.objects.create(
                product_name=f'fitness chicken{n}', slug=f'fitness-chicken{n}',
                price=120, product_image='good chicken', category_id=category.id
            )
        products = Product.objects.all()

        block_title = BlockTitle.objects.create(title='new products')
        cls.new_product = NewProducts.objects.create(
            title_id=block_title.id, product_1_id=products[0].id, image_prod1_active='image1_active',
            image_prod1='image1', product_2_id=products[1].id, image_prod2_active='image2_active', image_prod2='image2'
        )

    def test_new_products_model_entry(self):
        """Test NewProducts model data insertion/types/field attributes"""
        data = self.new_product
        self.assertTrue(isinstance(data, NewProducts))

    def test_new_products_model_name(self):
        """Tests NewProducts name"""
        data = self.new_product
        self.assertEqual(
            str(data),
            f'Секція: '
            f'{self.new_product.product_1}, '
            f'{self.new_product.product_2}'
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
                price=120, product_image='good chicken', category_id=category.id
            )
        products = Product.objects.all()

        block_title = BlockTitle.objects.create(title='most popular products')
        cls.most_popular_left = MostPopularLeft.objects.create(
            title_id=block_title.id, product_1_id=products[0].id, image_prod1_active='image1_active',
            image_prod1='image1', product_2_id=products[1].id, image_prod2_active='image2_active', image_prod2='image2',
            product_3_id=products[2].id, image_prod3_active='image3_active', image_prod3='image3'
        )

    def test_most_popular_left_model_entry(self):
        """Test MostPopularLeft model data insertion/types/field attributes"""
        data = self.most_popular_left
        self.assertTrue(isinstance(data, MostPopularLeft))

    def test_most_popular_left_model_name(self):
        """Tests MostPopularLeft name"""
        data = self.most_popular_left
        self.assertEqual(
            str(data),
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
                price=120, product_image='good chicken', category_id=category.id
            )
        products = Product.objects.all()

        block_title = BlockTitle.objects.create(title='most popular products')
        cls.most_popular_center = MostPopularCenter.objects.create(
            title_id=block_title.id, product_1_id=products[0].id, image_prod1_active='image1_active',
            image_prod1='image1', product_2_id=products[1].id, image_prod2_active='image2_active', image_prod2='image2',
            product_3_id=products[2].id, image_prod3_active='image3_active', image_prod3='image3'
        )

    def test_most_popular_center_model_entry(self):
        """Test MostPopularCenter model data insertion/types/field attributes"""
        data = self.most_popular_center
        self.assertTrue(isinstance(data, MostPopularCenter))

    def test_most_popular_center_model_name(self):
        """Tests MostPopularCenter name"""
        data = self.most_popular_center
        self.assertEqual(
            str(data),
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
                price=120, product_image='good chicken', category_id=category.id
            )
        products = Product.objects.all()

        block_title = BlockTitle.objects.create(title='most popular products')
        cls.most_popular_right = MostPopularRight.objects.create(
            title_id=block_title.id, product_1_id=products[0].id, image_prod1_active='image1_active',
            image_prod1='image1', product_2_id=products[1].id, image_prod2_active='image2_active', image_prod2='image2',
            product_3_id=products[2].id, image_prod3_active='image3_active', image_prod3='image3'
        )

    def test_most_popular_right_model_entry(self):
        """Test MostPopularRight model data insertion/types/field attributes"""
        data = self.most_popular_right
        self.assertTrue(isinstance(data, MostPopularRight))

    def test_most_popular_right_model_name(self):
        """Tests MostPopularRight name"""
        data = self.most_popular_right
        self.assertEqual(
            str(data),
            f'Секція: {self.most_popular_right.product_1}, '
            f'{self.most_popular_right.product_2}, '
            f'{self.most_popular_right.product_3}'
        )
