import json

import pytz
from crispy_forms.utils import render_crispy_form
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.context_processors import csrf
from django.utils import formats, timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import ModelFormMixin

from blog.forms import PostCommentForm
from blog.models import BlogCategory, Post, PostComment
from telebot.telegram import (
    send_to_telegram_moderate_new_comment_message,
    send_to_telegram_moderate_updated_comment_message,
)


class BlogPageView(ListView):
    """Rendering all blogs in the blog page"""
    model = Post
    template_name = 'blog/blog.html'
    queryset = Post.objects.all().filter(is_available=True).order_by('-created_date')
    context_object_name = 'posts'
    paginate_by = 9

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = self.queryset


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
    """Render a single post details page with PostComment form"""
    template_name = 'blog/post_details.html'
    form_class = PostCommentForm

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
        context['comments'] = PostComment.objects.filter(post=self.single_post, is_moderated=True)
        context['form'] = PostCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Processing the form through ajax. If the form is valid,
        then it calls the valid form processing method,
        if not, it displays errors using Crispy forms
        """
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if is_ajax:
            form = self.get_form()

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
        """
        Save a comment in the database, if it is a new,
        and overwrites it if there was already.
        """
        post = self.get_object()
        email = form.cleaned_data['email']

        try:
            # Update exists comment
            comment = PostComment.objects.get(post=post, email=email)
            comment.is_moderated = False
            form = PostCommentForm(self.request.POST, instance=comment)
            form.save()
            resp = {'update': True}

            # Send a message about the need to moderate a comment in Telegram
            send_to_telegram_moderate_updated_comment_message()

            return HttpResponse(json.dumps(resp), content_type='application/json')

        except ObjectDoesNotExist:
            # Save new comment
            comment_form = form.save(commit=False)
            comment_form.post = post
            form.save()
            resp = {'success': True}

            # Send a message about the need to moderate a comment in Telegram
            send_to_telegram_moderate_new_comment_message()

            return HttpResponse(json.dumps(resp), content_type='application/json')


class SearchListView(ListView):
    """Find posts by entered keyword in search string"""
    template_name = 'blog/blog.html'
    context_object_name = 'posts'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = None

    def get_queryset(self):
        """Filter posts by keyword"""
        if 'keyword' in self.request.GET:
            keyword = self.request.GET['keyword']
            self.object_list = Post.objects.order_by(
                '-created_date').filter(Q(title__icontains=keyword) |
                                        Q(description__icontains=keyword) |
                                        Q(quote__icontains=keyword))
        return self.object_list


def convert_to_localtime(utctime):
    """Convert UTC datetime format to local with Django project format"""
    utc_date = utctime.replace(tzinfo=pytz.UTC)
    local_date = utc_date.astimezone(timezone.get_current_timezone())
    return formats.date_format(local_date, "DATETIME_FORMAT")


def load_more_comments(request):
    """Pass to ajax comments for load by press Show more button"""
    if request.POST.get('action') == 'POST':
        post_id = int(request.POST.get('post_id'))
        visible_comments = int(request.POST.get('visible_comments'))

        upper = visible_comments
        lower = upper - 10

        post = get_object_or_404(Post, id=post_id)

        # Take comments starting from the fourth, since three are displayed immediately after page loading
        comments = list(PostComment.objects.filter(post=post, is_moderated=True)[3:].values()[lower:upper])
        for item in comments:
            item['modified_date'] = convert_to_localtime(item['modified_date'])

        comments_size = len(PostComment.objects.filter(post=post, is_moderated=True)[3:])
        max_size = True if upper >= comments_size else False

        return JsonResponse({'data': comments, 'max': max_size}, safe=False)
