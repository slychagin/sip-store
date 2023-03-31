from importlib import import_module
from urllib.parse import urlencode

from django.conf import settings
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from blog.forms import PostCommentForm
from blog.models import BlogCategory, Post, PostComment
from blog.views import (BlogPageView, PostDetailView, PostsByCategoryListView,
                        SearchListView)
from telebot.models import TelegramSettings


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

        # Create category and post
        self.blog_category = BlogCategory.objects.create(
            category_name='fresh posts', slug='fresh-posts'
        )
        self.post = Post.objects.create(
            title='Post 1', post_image='image', mini_image='image',
            post_category=self.blog_category
        )

        # Create telegram settings in the database
        TelegramSettings.objects.create(
            tg_token='token12345',
            tg_chat='123456',
            tg_api='telegram_api_key'
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

    def test_post_detail_view_post_method_with_invalid_form(self):
        """
        Tests post method. Check PostCommentForm. Show form errors.
        """
        data = {
            'name': 'Sergio',
            'email': '',
            'content': 'Lorem ipsum dolor sit amet'
        }

        response = self.client.post(
            reverse('post_details', args=[self.blog_category.slug, self.post.id]),
            data=urlencode(data),
            xhr=True,
            content_type='application/x-www-form-urlencoded',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertFormError(response.context['form'], 'email', "Це поле обов'язкове.")

    def test_post_method_with_valid_form_new_comment(self):
        """
        Tests post method. Check PostCommentForm. If the user
        not leave comment for this post than create and
        save in the database new comment.
        """
        data = {
            'name': 'Sergio',
            'email': 'email@gmail.com',
            'content': 'Lorem ipsum dolor sit amet'
        }

        response = self.client.post(
            reverse('post_details', args=[self.blog_category.slug, self.post.id]),
            data=urlencode(data),
            xhr=True,
            content_type='application/x-www-form-urlencoded',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        comment = PostComment.objects.get(post=self.post, email=data['email'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        self.assertTrue(comment)

    def test_post_method_with_valid_form_update_comment(self):
        """
        Tests post method. Check PostCommentForm. If the user
        leave comment for this post than update comment.
        """
        data = {
            'name': 'Sergio',
            'email': 'email@gmail.com',
            'content': 'Awsome post!'
        }

        # Create a comment to emulate the comment update script
        PostComment.objects.create(
            post=self.post, name='Sergio', email='email@gmail.com', content='Bad post!'
        )

        response = self.client.post(
            reverse('post_details', args=[self.blog_category.slug, self.post.id]),
            data=urlencode(data),
            xhr=True,
            content_type='application/x-www-form-urlencoded',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        comments = PostComment.objects.filter(post=self.post, email=data['email'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'update': True})
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0].name, 'Sergio')
        self.assertEqual(comments[0].email, 'email@gmail.com')
        self.assertEqual(comments[0].content, 'Awsome post!')


class SearchListViewTest(TestCase):
    """Tests SearchListView"""

    @classmethod
    def setUpTestData(cls):
        """Create client, category and post objects"""
        cls.client = Client()
        cls.factory = RequestFactory()
        cls.view = SearchListView()

        # Create category and posts
        cls.category = BlogCategory.objects.create(
            category_name='fresh posts', slug='fresh-posts'
        )
        category_id = BlogCategory.objects.get(category_name='fresh posts').id
        cls.post_1 = Post.objects.create(
            title='Post about chicken', post_image='image1', mini_image='image4',
            description='Good morning!', quote='Beautiful day!', post_category_id=category_id
        )
        cls.post_2 = Post.objects.create(
            title='Post about pork', post_image='image2', mini_image='image5',
            description='Good afternoon!', quote='Wonderful day!', post_category_id=category_id
        )
        cls.post_3 = Post.objects.create(
            title='Post about ham', post_image='image3', mini_image='image6',
            description='Good evening!', quote='Awsome day!', post_category_id=category_id
        )

    def test_search_list_view_url_exists_at_desired_location(self):
        """Tests that search list view url exists at desired location"""
        response = self.client.get('/blog/search-post/')
        self.assertEqual(response.status_code, 200)

    def test_search_list_view_url_accessible_by_name(self):
        """Tests search list view url accessible by name"""
        response = self.client.get(reverse('search_post'))
        self.assertEqual(response.status_code, 200)

    def test_search_list_view_uses_correct_template(self):
        """Tests search list view uses correct template"""
        response = self.client.get(reverse('search_post'))
        self.assertTemplateUsed(response, 'blog/blog.html')

    def test_search_list_view_html(self):
        """Test SearchListView html"""
        request = self.factory.get('/blog/search-post/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf-8')

        self.assertIn(str(self.category), html)
        self.assertIn(str(self.post_1), html)
        self.assertIn(str(self.post_2), html)
        self.assertIn(str(self.post_3), html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_context_with_empty_search_string(self):
        """Tests SearchListView context with empty search string"""
        request = self.factory.get('/blog/search-post/')
        self.view.setup(request)
        context = self.view.get_context_data()
        self.assertTrue(context['posts'] is None)

    def test_context_with_unique_post_title_in_search_string(self):
        """
        Tests SearchListView context with unique word in post title
        that was entered in search string
        """
        request = self.factory.get('/blog/search-post/?keyword=chicken')
        self.view.setup(request)
        self.view.get_queryset()
        context = self.view.get_context_data()

        self.assertEqual(len(context['posts']), 1)
        self.assertIn(self.post_1, context['posts'])

    def test_context_with_unique_description_in_search_string(self):
        """
        Tests SearchListView context with unique word in post
        description that was entered in search string
        """
        request = self.factory.get('/blog/search-post/?keyword=afternoon')
        self.view.setup(request)
        self.view.get_queryset()
        context = self.view.get_context_data()

        self.assertEqual(len(context['posts']), 1)
        self.assertIn(self.post_2, context['posts'])

    def test_context_with_unique_quote_in_search_string(self):
        """
        Tests SearchListView context with unique word in post
        quote that was entered in search string
        """
        request = self.factory.get('/blog/search-post/?keyword=wonderful')
        self.view.setup(request)
        self.view.get_queryset()
        context = self.view.get_context_data()

        self.assertEqual(len(context['posts']), 1)
        self.assertIn(self.post_2, context['posts'])

    def test_context_with_recurring_title_in_search_string(self):
        """
        Tests SearchListView context with recurring word in post title
        that was entered in search string
        """
        request = self.factory.get('/blog/search-post/?keyword=post')
        self.view.setup(request)
        self.view.get_queryset()
        context = self.view.get_context_data()

        self.assertEqual(len(context['posts']), 3)
        self.assertIn(self.post_1, context['posts'])
        self.assertIn(self.post_2, context['posts'])
        self.assertIn(self.post_3, context['posts'])

    def test_context_with_recurring_description_in_search_string(self):
        """
        Tests SearchListView context with recurring word in post
        description that was entered in search string
        """
        request = self.factory.get('/blog/search-post/?keyword=good')
        self.view.setup(request)
        self.view.get_queryset()
        context = self.view.get_context_data()

        self.assertEqual(len(context['posts']), 3)
        self.assertIn(self.post_1, context['posts'])
        self.assertIn(self.post_2, context['posts'])
        self.assertIn(self.post_3, context['posts'])

    def test_context_with_recurring_quote_in_search_string(self):
        """
        Tests SearchListView context with recurring word in post quote
        that was entered in search string
        """
        request = self.factory.get('/blog/search-post/?keyword=day')
        self.view.setup(request)
        self.view.get_queryset()
        context = self.view.get_context_data()

        self.assertEqual(len(context['posts']), 3)
        self.assertIn(self.post_1, context['posts'])
        self.assertIn(self.post_2, context['posts'])
        self.assertIn(self.post_3, context['posts'])


class LoadMoreCommentsTest(TestCase):
    """Tests load more comments function"""

    def setUp(self):
        """Create category, products and reviews objects"""
        self.client = Client()
        self.category = BlogCategory.objects.create(
            category_name='fresh posts', slug='fresh-posts'
        )
        self.post = Post.objects.create(
            title='Post about chicken', post_image='image1', mini_image='image4',
            description='Good morning!', quote='Beautiful day!', post_category=self.category
        )

        # Create 20 comments for product (3 comments are shown immediately
        # when the page is loaded and then, by pressing a button,
        # it shows 10 comments, press one more - 7 reviews)
        for i in range(20):
            PostComment.objects.create(
                post=self.post, name='Sergio', email=f'mail{i}@gmail.com',
                content='This is a good post!', is_moderated=True
            )

    def test_load_more_comments(self):
        """Test load more comments function"""
        # After the page loads, three comments are displayed. Hidden 17 comments.
        # Press button "show more comments" (show next 10 comments, left 7 comments)
        response = self.client.post(
            reverse('load_more_comments'),
            {'post_id': self.post.id, 'visible_comments': 10, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(len(response.json()['data']), 10)

        # Press button "show more comments" one more (show next 7 comments, left 0 comments)
        response = self.client.post(
            reverse('load_more_comments'),
            {'post_id': self.post.id, 'visible_comments': 20, 'action': 'POST'},
            xhr=True
        )
        self.assertEqual(len(response.json()['data']), 7)
