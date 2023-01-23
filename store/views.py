from django.shortcuts import render

from store.models import Product


def store(request):
    """Rendering store page"""
    products = Product.objects.all().filter(is_available=True, is_active=True)
    context = {
        'products': products
    }
    return render(request, 'store/store.html', context)
