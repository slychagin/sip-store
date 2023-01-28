from django.shortcuts import render, get_object_or_404

from category.models import Category
from store.models import Product


def store(request, category_slug=None):
    """Rendering store page"""
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
        'product_count': products.count()
    }
    return render(request, 'store/store.html', context)


def product_details(request, category_slug, product_slug):
    """Rendering product details page"""
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product
    }

    return render(request, 'store/product_details.html', context)



