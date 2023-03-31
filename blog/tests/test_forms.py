import time

from django import forms
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase, tag
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver

from blog.forms import PostCommentAdminForm, PostCommentForm
from blog.models import BlogCategory, Post, PostComment


class PostCommentFormTest(TestCase):
    """Tests PostCommentForm"""

    def test_form_fields_label(self):
        """Tests all labels in PostCommentForm"""
        form = PostCommentForm()
        self.assertTrue(
            form.fields['name'].label is None
            or form.fields['name'].label == "Ім'я"
        )
        self.assertTrue(
            form.fields['email'].label is None
            or form.fields['email'].label == 'Email'
        )
        self.assertTrue(
            form.fields['content'].label is None
            or form.fields['content'].label == 'Коментар'
        )

    def test_form_fields_title(self):
        """Tests all form fields titles"""
        form = PostCommentForm()
        for field in form.fields:
            self.assertEqual(
                form.fields[field].widget.attrs['title'],
                'Заповніть це поле')

    def test_form_clean_content_greater_1000_sings(self):
        """Tests content validation field by length"""
        # Text length - 1009 sings
        text = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla egestas elit turpis,
            sit amet luctus nisl suscipit ac. Donec non purus eu arcu sodales sodales ac eu leo.
            Mauris eleifend quis metus dapibus congue. Etiam tincidunt, libero ac venenatis
            tempus, ipsum neque pellentesque neque, et euismod purus nisi vel lectus. Donec
            imperdiet ut ante ut feugiat. Aliquam interdum eget nisi ut pellentesque. Mauris
            tincidunt semper lorem in blandit. Quisque vel mi quam. Ut eu urna posuere,
            ultricies ipsum nec, rhoncus justo. Curabitur viverra nulla vel justo euismod,
            id tincidunt mi fringilla. Ut tempor et mauris ac placerat. Ut pellentesque
            luctus enim, dapibus tempor tortor vulputate vel. Donec eu commodo ante.
            Vestibulum sagittis, neque sed dignissim maximus, dui neque facilisis velit,
            in laoreet est risus a sapien. Vivamus at elit id augue congue accumsan quis
            nec nibh.
        """

        form = PostCommentForm(data={
            'name': 'Serhio',
            'email': 'email@gmail.com',
            'content': text
        })
        self.assertFalse(form.is_valid())

    def test_form_clean_content_less_1000_sings(self):
        """Tests content validation field by length"""
        text = """
             Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla egestas
             elit turpis, sit amet luctus nisl suscipit ac.
        """

        form = PostCommentForm(data={
            'name': 'Serhio',
            'email': 'email@gmail.com',
            'content': text
        })
        self.assertTrue(form.is_valid())


class PostCommentAdminFormTest(TestCase):
    """Tests PostCommentAdminForm"""

    def setUp(self):
        """Create blog category, post and post comment objects"""
        self.blog_category = BlogCategory.objects.create(
            category_name='fresh posts', slug='fresh-posts'
        )
        self.post = Post.objects.create(
            title='Post 1', post_image='image', mini_image='image', post_category=self.blog_category
        )
        self.post_comment = PostComment.objects.create(
            post=self.post, name='Sergio', email='email@gmail.com', content='Post content'
        )

    def test_clean_method_invalid_form(self):
        """
        Tests that form rase error if administrator entered
        comment for post in admin panel with not unique email
        """
        form = PostCommentAdminForm(data={
            'post': self.post,
            'name': 'Serhio',
            'email': 'email@gmail.com',
            'content': 'New comment!'
        })
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(
            forms.ValidationError,
            'Коментар з таким email до даного посту вже існує.'
        )

    def test_clean_method_valid_form(self):
        """
        Tests that form valid if administrator entered
        comment for post in admin panel with unique email
        """
        form = PostCommentAdminForm(data={
            'post': self.post,
            'name': 'Serhio',
            'email': 'sergio@gmail.com',
            'content': 'New comment!'
        })
        self.assertTrue(form.is_valid())


@tag('selenium')
class PostCommentFormSeleniumTest(StaticLiveServerTestCase):
    """Test PostCommentForm by Selenium"""
    selenium = None

    def setUp(self):
        """Create blog category and post objects"""
        self.blog_category = BlogCategory.objects.create(
            category_name='fresh', slug='fresh'
        )
        self.post = Post.objects.create(
            title='Post 1', post_image='image',
            mini_image='image', post_category=self.blog_category
        )

    @classmethod
    def setUpClass(cls):
        """Setup Firefox webdriver"""
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        """Shutdown webdriver"""
        cls.selenium.quit()
        super().tearDownClass()

    def test_post_comment_form_by_selenium(self):
        """Emulate filling and submit post form by user"""
        self.selenium.get(f'{self.live_server_url}/blog/category/{self.blog_category.slug}/{self.post.id}/')
        time.sleep(2)

        name_input = self.selenium.find_element(By.NAME, 'name')
        email_input = self.selenium.find_element(By.NAME, 'email')
        content_input = self.selenium.find_element(By.NAME, 'content')
        time.sleep(2)

        submit = self.selenium.find_element(By.ID, 'ajax_comment')

        name_input.send_keys('Sergio')
        email_input.send_keys('super@gmail.com')
        content_input.send_keys('Super post!')

        submit.send_keys(Keys.RETURN)
        time.sleep(2)

        new_comment = PostComment.objects.all()[0]
        self.assertTrue(new_comment)
