import json

from crispy_forms.utils import render_crispy_form
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.context_processors import csrf
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import ModelFormMixin

from blog.forms import CommentForm
from blog.models import Post, BlogCategory


class BlogPageView(ListView):
    """Rendering all blogs in the blog page"""
    model = Post
    template_name = 'blog/blog.html'
    queryset = Post.objects.all().filter(is_available=True).order_by('-created_date')
    context_object_name = 'posts'
    paginate_by = 9


class PostsByCategoryListView(ListView):
    """Rendering posts by category in the blog page"""
    template_name = 'blog/blog.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.posts = None
        self.categories = None
        self.slug = None

    def get_queryset(self):
        """Return posts by category"""
        self.categories = get_object_or_404(BlogCategory, slug=self.kwargs['slug'])
        self.posts = Post.objects.filter(post_category=self.categories, is_available=True)
        return self.posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.posts
        return context


class PostDetailView(ModelFormMixin, DetailView):
    """Render a single post details page"""
    template_name = 'blog/post_details.html'
    form_class = CommentForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None
        self.category_slug = None
        self.post_id = None
        self.single_post = None

    def get_object(self, **kwargs):
        """Return single post by category and post id"""
        self.single_post = get_object_or_404(
            Post,
            post_category__slug=self.kwargs['slug'],
            id=self.kwargs['pk']
        )

        return self.single_post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        related_posts = Post.related_posts.through.objects.filter(from_post_id=self.single_post.id)
        context['single_post'] = self.single_post
        context['related_posts'] = [item.to_post for item in related_posts]
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if is_ajax:
            form = self.get_form()
            self.object = self.get_object()
            if form.is_valid():
                return self.form_valid(form)
            else:
                resp = {'success': False}
                csrf_context = {}
                csrf_context.update(csrf(request))
                comment_form = render_crispy_form(form, context=csrf_context)
                resp['html'] = comment_form
            return HttpResponse(json.dumps(resp), content_type='application/json')

    def form_valid(self, form):
        post = self.get_object()
        comment_form = form.save(commit=False)
        comment_form.post = post
        form.save()
        resp = {'success': True}




        return HttpResponse(json.dumps(resp), content_type='application/json')

    def get_success_url(self):
        return reverse('post_details', kwargs={
            'slug': self.object.post.post_category.slug,
            'pk': self.object.post.pk
        })




















# class PostDetailView(ModelFormMixin, DetailView):
#     """Render a single post details page"""
#     template_name = 'blog/post_details.html'
#     form_class = CommentForm
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.object = None
#         self.category_slug = None
#         self.post_id = None
#         self.single_post = None
#
#     def get_object(self, **kwargs):
#         """Return single post by category and post id"""
#         self.single_post = get_object_or_404(
#             Post,
#             post_category__slug=self.kwargs['slug'],
#             id=self.kwargs['pk']
#         )
#
#         return self.single_post
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         related_posts = Post.related_posts.through.objects.filter(from_post_id=self.single_post.id)
#         context['single_post'] = self.single_post
#         context['related_posts'] = [item.to_post for item in related_posts]
#         context['form'] = CommentForm()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         self.object = self.get_object()
#
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_valid(self, form):
#         post = self.get_object()
#         comment_form = form.save(commit=False)
#         comment_form.post = post
#         form.save()
#         return super(PostDetailView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse('post_details', kwargs={
#             'slug': self.object.post.post_category.slug,
#             'pk': self.object.post.pk
#         })






class SearchListView(ListView):
    """Find posts by keyword"""
    template_name = 'blog/blog.html'
    context_object_name = 'posts'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.posts = None

    def get_queryset(self):
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
            self.posts = Post.objects.order_by(
                '-created_date').filter(Q(title__icontains=keyword) |
                                        Q(description__icontains=keyword) |
                                        Q(quote__icontains=keyword))
        return self.posts
