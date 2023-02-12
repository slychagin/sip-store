from django.shortcuts import render
from django.views.generic import ListView


def blog_page(request):
    """Rendering all blogs in the blog page"""
    return render(request, 'blog/blog.html')

# class BlogPageView(ListView):
#     """Rendering all blogs in the blog page"""
#     template_name = 'blog/blog.html'

