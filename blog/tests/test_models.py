from datetime import date

from django.test import TestCase

from blog.models import BlogCategory, Post, PostComment, Tag
from category.models import Category
from store.models import Product


class BlogCategoryModelTest(TestCase):
    """Tests BlogCategory model"""

    @classmethod
    def setUpTestData(cls):
        """Create BlogCategory object"""
        cls.blog_category = BlogCategory.objects.create(category_name='pork', slug='pork')

    def test_blog_category_model_entry(self):
        """
        Test that created blog category object is
        instance of BlogCategory model
        """
        self.assertTrue(isinstance(self.blog_category, BlogCategory))

    def test_blog_category_model_name(self):
        """Test BlogCategory object name"""
        self.assertEqual(str(self.blog_category), 'pork')

    def test_get_absolute_url(self):
        """Test absolute url for BlogCategory object"""
        self.assertEqual(self.blog_category.get_url(), '/blog/category/pork/')

    def test_blog_category_fields_max_length(self):
        """Test category fields max length"""
        data = self.blog_category
        category_name_max_length = data._meta.get_field('category_name').max_length
        slug_max_length = data._meta.get_field('slug').max_length

        self.assertEqual(category_name_max_length, 100)
        self.assertEqual(slug_max_length, 100)

    def test_blog_category_fields_label(self):
        """Test BlogCategory fields verbose name"""
        data = self.blog_category

        category_name = data._meta.get_field('category_name').verbose_name
        slug = data._meta.get_field('slug').verbose_name
        description = data._meta.get_field('description').verbose_name
        category_image = data._meta.get_field('category_image').verbose_name

        self.assertEqual(category_name, 'найменування категорії')
        self.assertEqual(slug, 'написання в URL')
        self.assertEqual(description, 'опис')
        self.assertEqual(category_image, 'фото категорії')


class TagModelTest(TestCase):
    """Tests Tag model"""

    @classmethod
    def setUpTestData(cls):
        """Create Tag object"""
        category = Category.objects.create(category_name='chicken', slug='chicken')
        product = Product.objects.create(
            product_name='pork', slug='pork', price=100,
            product_image='good pork', category=category
        )
        cls.tag = Tag.objects.create(name='fresh', product=product)

    def test_tag_entry(self):
        """
        Test that created tag object is instance of Tag model
        """
        self.assertTrue(isinstance(self.tag, Tag))

    def test_tag_model_name(self):
        """Tests Tag object name"""
        self.assertEqual(str(self.tag), 'fresh')

    def test_tag_fields_max_length(self):
        """Test Tag fields max length"""
        data = self.tag
        name_max_length = data._meta.get_field('name').max_length
        self.assertEqual(name_max_length, 100)

    def test_tag_labels(self):
        """Test Tag verbose names"""
        data = self.tag
        name = data._meta.get_field('name').verbose_name
        product = data._meta.get_field('product').verbose_name

        self.assertEqual(name, 'назва тегу')
        self.assertEqual(product, 'продукт')


class PostModelTest(TestCase):
    """Tests Post model"""

    @classmethod
    def setUpTestData(cls):
        """Create Post object"""
        category = BlogCategory.objects.create(category_name='chicken', slug='chicken')
        cls.post = Post.objects.create(
            title='post', mini_image='mini_image', post_category=category
        )

    def test_post_model_entry(self):
        """
        Test that created Post object is instance of Post model
        """
        self.assertTrue(isinstance(self.post, Post))

    def test_post_model_name(self):
        """Tests Post object name"""
        self.assertEqual(str(self.post), 'post')

    def test_get_url(self):
        """Test absolute url for Post object"""
        self.assertEqual(self.post.get_url(), f'/blog/category/chicken/{self.post.id}/')

    def test_post_created_date(self):
        """Test Post object post_created_date"""
        data = self.post
        post_date = data.post_created_date
        today_date = date.today()

        self.assertEqual(post_date, today_date)

    def test_recent_created_date(self):
        """Test Post object recent_created_date"""
        data = self.post
        post_date = data.recent_created_date
        today_date = date.today().strftime('%d/%m/%Y')

        self.assertEqual(post_date, today_date)

    def test_post_fields_max_length(self):
        """Test Post fields max length"""
        data = self.post

        title_name_max_length = data._meta.get_field('title').max_length
        banner_url_max_length = data._meta.get_field('banner_url').max_length
        related_posts_title_max_length = data._meta.get_field('related_posts_title').max_length

        self.assertEqual(title_name_max_length, 255)
        self.assertEqual(banner_url_max_length, 255)
        self.assertEqual(related_posts_title_max_length, 255)

    def test_post_labels(self):
        """Test Post verbose names"""
        data = self.post

        title = data._meta.get_field('title').verbose_name
        description = data._meta.get_field('description').verbose_name
        quote = data._meta.get_field('quote').verbose_name
        post_image = data._meta.get_field('post_image').verbose_name
        mini_image = data._meta.get_field('mini_image').verbose_name
        banner_url = data._meta.get_field('banner_url').verbose_name
        is_available = data._meta.get_field('is_available').verbose_name
        created_date = data._meta.get_field('created_date').verbose_name
        modified_date = data._meta.get_field('modified_date').verbose_name
        post_category = data._meta.get_field('post_category').verbose_name
        tags = data._meta.get_field('tags').verbose_name
        related_posts_title = data._meta.get_field('related_posts_title').verbose_name
        related_posts = data._meta.get_field('related_posts').verbose_name

        self.assertEqual(title, 'тема поста')
        self.assertEqual(description, 'опис поста')
        self.assertEqual(quote, 'цитата до посту')
        self.assertEqual(post_image, 'фото до посту')
        self.assertEqual(mini_image, 'міні фото до посту')
        self.assertEqual(banner_url, 'URL переходу')
        self.assertEqual(is_available, 'доступний')
        self.assertEqual(created_date, 'дата створення')
        self.assertEqual(modified_date, 'дата змін')
        self.assertEqual(post_category, 'категорія')
        self.assertEqual(tags, 'теги')
        self.assertEqual(related_posts_title, 'заголовок до схожих постів')
        self.assertEqual(related_posts, 'схожі пости')


class PostCommentModelTest(TestCase):
    """Tests PostComment model"""

    @classmethod
    def setUpTestData(cls):
        """Create PostComment object"""
        category = BlogCategory.objects.create(category_name='chicken', slug='chicken')
        post = Post.objects.create(
            title='post', mini_image='mini_image', post_category=category
        )
        cls.post_comment = PostComment.objects.create(
            post=post, name='Serg', email='email@gmail.com', content='Good Post'
        )

    def test_post_comment_model_entry(self):
        """
        Test that created PostComment object is instance of PostComment model
        """
        self.assertTrue(isinstance(self.post_comment, PostComment))

    def test_post_comment_model_name(self):
        """Tests PostComment object name"""
        self.assertEqual(str(self.post_comment), 'post')

    def test_post_comment_fields_max_length(self):
        """Test PostComment fields max length"""
        data = self.post_comment

        name_name_max_length = data._meta.get_field('name').max_length
        email_url_max_length = data._meta.get_field('email').max_length

        self.assertEqual(name_name_max_length, 80)
        self.assertEqual(email_url_max_length, 100)

    def test_post_comment_labels(self):
        """Test PostComment verbose names"""
        data = self.post_comment

        post = data._meta.get_field('post').verbose_name
        name = data._meta.get_field('name').verbose_name
        email = data._meta.get_field('email').verbose_name
        content = data._meta.get_field('content').verbose_name
        created_date = data._meta.get_field('created_date').verbose_name
        modified_date = data._meta.get_field('modified_date').verbose_name
        is_moderated = data._meta.get_field('is_moderated').verbose_name

        self.assertEqual(post, 'пост')
        self.assertEqual(name, "ім'я")
        self.assertEqual(email, 'E-mail')
        self.assertEqual(content, 'коментар')
        self.assertEqual(created_date, 'дата створення')
        self.assertEqual(modified_date, 'дата коригування')
        self.assertEqual(is_moderated, 'промодерований')
