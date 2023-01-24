from category.models import Category


def menu_links(request):
    """
    Get links for all categories in database.
    After that we can use this links in templates anywhere in the project.
    """
    category_links = Category.objects.all().order_by('category_name')
    return dict(category_links=category_links)
