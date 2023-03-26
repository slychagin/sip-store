from importlib import import_module

from django.conf import settings
from django.test import (
    TestCase,
    Client,
    RequestFactory
)
from django.urls import reverse

from blog.forms import PostCommentForm
from blog.models import BlogCategory, Post
from blog.views import (
    BlogPageView,
    PostsByCategoryListView,
    PostDetailView
)


class BlogPageViewTest(TestCase):
    """Tests BlogPageView"""

    @classmethod
    def setUpTestData(cls):
        """
        Create blog category and 15 posts object for check pagination
        """
        number_of_posts = 15
        blog_category = BlogCategory.objects.create(
            category_name='big posts', slug='big-posts'
        )

        for post_id in range(number_of_posts):
            Post.objects.create(
                title=f'Post {post_id}',
                post_image='image',
                mini_image='image',
                post_category=blog_category
            )

    def setUp(self):
        """Create blog category and post object"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = BlogPageView()

        self.blog_category = BlogCategory.objects.create(category_name='fresh posts', slug='fresh-posts')
        self.post = Post.objects.create(
            title='Post 1', post_image='image', mini_image='image', post_category=self.blog_category
        )

    def test_blog_page_view_url_exists_at_desired_location(self):
        """Tests that blog page view url exists at desired location"""
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_blog_page_view_url_accessible_by_name(self):
        """Tests blog page view url accessible by name"""
        response = self.client.get(reverse('blog_page'))
        self.assertEqual(response.status_code, 200)

    def test_blog_page_view_uses_correct_template(self):
        """Tests blog page view uses correct template"""
        response = self.client.get(reverse('blog_page'))
        self.assertTemplateUsed(response, 'blog/blog.html')

    def test_blog_page_html(self):
        """Test BlogPage html"""
        request = self.factory.get('/blog/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf-8')

        self.assertIn(str(self.blog_category), html)
        self.assertIn(str(self.post), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_blog_page_view_context(self):
        """Tests BlogPageView context"""
        request = self.factory.get('/blog/')
        self.view.setup(request)
        context = self.view.get_context_data()

        self.assertTrue(len(context['posts']) == 9)
        self.assertIn(self.post, context['object_list'])

    def test_blog_pagination_is_nine(self):
        """Get first page and check that it have 9 post"""
        response = self.client.get(reverse('blog_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['posts']), 9)

    def test_lists_all_posts(self):
        """Get second page and confirm it has (exactly) remaining 6 items"""
        response = self.client.get(reverse('blog_page') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['posts']), 7)


class PostsByCategoryListViewTest(TestCase):
    """Tests PostsByCategoryListView class-based view"""

    def setUp(self):
        """Create blog category and post object"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = PostsByCategoryListView()

        self.blog_category = BlogCategory.objects.create(category_name='fresh posts', slug='fresh-posts')
        self.post = Post.objects.create(
            title='Post 1', post_image='image', mini_image='image', post_category=self.blog_category
        )

    def test_posts_by_category_list_view_url_exists_at_desired_location(self):
        """Tests that posts by category view url exists at desired location"""
        response = self.client.get('/blog/category/fresh-posts/')
        self.assertEqual(response.status_code, 200)

    def test_posts_by_category_list_view_url_accessible_by_name(self):
        """Tests posts by category view url accessible by name"""
        response = self.client.get(reverse('posts_by_category', args=['fresh-posts']))
        self.assertEqual(response.status_code, 200)

    def test_posts_by_category_list_view_uses_correct_template(self):
        """Tests posts by category view uses correct template"""
        response = self.client.get(reverse('posts_by_category', args=['fresh-posts']))
        self.assertTemplateUsed(response, 'blog/blog.html')

    def test_posts_by_category_list_view(self):
        """Test posts by category view"""
        request = self.factory.get('/blog/fresh-blog/')
        self.view.setup(request)
        response = self.client.get(reverse('posts_by_category', args=['fresh-posts']))
        html = response.content.decode('utf-8')

        self.assertIn(str(self.blog_category), html)
        self.assertIn(str(self.post), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_posts_by_category_list_view_context(self):
        """Tests posts by category view context"""
        response = self.client.get(reverse('posts_by_category', args=['fresh-posts']))
        context = response.context

        self.assertTrue(len(context['posts']) == 1)
        self.assertEqual(response.status_code, 200)


class PostDetailViewTest(TestCase):
    """Tests PostDetailView class-based view"""

    def setUp(self):
        """Create category and post object"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = PostDetailView()

        self.blog_category = BlogCategory.objects.create(category_name='fresh posts', slug='fresh-posts')
        self.post = Post.objects.create(
            title='Post 1', post_image='image', mini_image='image', post_category=self.blog_category
        )

    def test_post_detail_view_url_exists_at_desired_location(self):
        """Tests that post detail view url exists at desired location"""
        response = self.client.get(f'/blog/category/fresh-posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_post_details_view_url_accessible_by_name(self):
        """Tests post details view url accessible by name"""
        response = self.client.get(
            reverse('post_details', args=['fresh-posts', f'{self.post.id}'])
        )
        self.assertEqual(response.status_code, 200)

    def test_post_details_view_uses_correct_template(self):
        """Tests post details view uses correct template"""
        response = self.client.get(
            reverse('post_details', args=['fresh-posts', f'{self.post.id}'])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_details.html')

    def test_post_details_view(self):
        """Test post details class-based view"""
        request = self.factory.get(f'/blog/fresh-posts/{self.post.id}/')
        self.view.setup(request)
        response = self.client.get(
            reverse('post_details', args=['fresh-posts', f'{self.post.id}'])
        )
        html = response.content.decode('utf8')

        self.assertIn(str(self.blog_category), html)
        self.assertIn(str(self.post), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_post_details_view_context(self):
        """Tests post details view context"""
        response = self.client.get(
            reverse('post_details', args=['fresh-posts', f'{self.post.id}']))
        context = response.context

        self.assertEqual(response.status_code, 200)
        self.assertTrue('single_post' in context)
        self.assertEqual(context['single_post'].title, 'Post 1')
        self.assertTrue(isinstance(context['form'], PostCommentForm))

    def test_post_details_page_not_found(self):
        request = self.factory.get('/blog/not-found/not-found/')
        self.view.setup(request)
        response = self.client.get(
            reverse('post_details', args=['fresh-posts', f'{self.post.id}1'])
        )
        self.assertEqual(response.status_code, 404)

