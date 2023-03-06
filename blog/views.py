from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

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


class PostDetailView(DetailView):
    """Render a single post details page"""
    template_name = 'blog/post_details.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.category_slug = None
        self.post_id = None
        self.single_post = None

    def get_object(self, **kwargs):
        """Return single post by category and post id"""
        try:
            self.single_post = Post.objects.get(
                post_category__slug=self.kwargs['slug'],
                id=self.kwargs['pk']
            )
        except ObjectDoesNotExist:
            raise Http404('Сторінку не знайдено')

        return self.single_post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['single_post'] = self.single_post
        return context


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
