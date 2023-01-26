from django.shortcuts import render

from benefits.models import Benefits
from sales.models import BestSellers, NewProducts


def home(request):
    """Rendering home page"""
    benefits = Benefits.objects.all()
    bestsellers = BestSellers.objects.all()
    new_products = NewProducts.objects.all()

    context = {
        'benefits': benefits,
        'bestsellers': bestsellers,
        'new_products': new_products
    }
    return render(request, 'sip/home.html', context)
