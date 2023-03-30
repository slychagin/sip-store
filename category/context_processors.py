from category.models import Category
from store.models import Product


def menu_links(request):
    """
    Get links for all categories in database.
    After that we can use this links in templates anywhere in the project.
    """
    category_links = Category.objects.all()
    product_links = [
        Product.objects.filter(category=category, is_available=True).order_by('created_date')
        for category in category_links
    ]
    return dict(category_links=category_links, product_links=product_links)
