from category.models import Category
from store.models import Product


def menu_links(request):
    """
    Get links for all categories in database.
    After that we can use this links in templates anywhere in the project.
    """
    category_links = Category.objects.all().order_by('category_name')
    product_links = [Product.objects.all().filter(category=category).order_by('product_name') for category in category_links]
    return dict(category_links=category_links, product_links=product_links)
