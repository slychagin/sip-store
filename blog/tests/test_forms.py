from django import forms
from django.test import TestCase

from blog.forms import PostCommentForm, PostCommentAdminForm
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
            nec nibh. Sed sed mollis turpis. Phasellus feugiat justo dui, malesuada posuere
            ligula porta nec. Vivamus condimentum elit justo quam.
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
        self.assertRaises(forms.ValidationError)

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
