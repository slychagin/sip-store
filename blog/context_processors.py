from blog.models import BlogCategory, Post, PostComment, Tag


def blog_sidebar(request):
    """Get info for blog sidebar"""
    blog_categories = BlogCategory.objects.all().order_by('category_name')
    post_tags = Tag.objects.all().order_by('name')
    recent_posts = Post.objects.all().order_by('-modified_date')[:3]
    recent_home_posts = Post.objects.all().order_by('-modified_date')[:6]
    recent_comments = PostComment.objects.filter(is_moderated=True).order_by('-modified_date')[:3]
    return dict(
        blog_categories=blog_categories,
        post_tags=post_tags,
        recent_posts=recent_posts,
        recent_home_posts=recent_home_posts,
        recent_comments=recent_comments
    )
