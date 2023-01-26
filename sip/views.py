from django.shortcuts import render

from benefits.models import Benefits
from sales.models import (
    BestSellers,
    NewProducts,
    MostPopularLeft,
    MostPopularCenter,
    MostPopularRight
)


def home(request):
    """Rendering home page"""
    benefits = Benefits.objects.all()
    bestsellers = BestSellers.objects.all()
    new_products = NewProducts.objects.all()
    popular_left = MostPopularLeft.objects.all()
    popular_center = MostPopularCenter.objects.all()
    popular_right = MostPopularRight.objects.all()

    context = {
        'benefits': benefits,
        'bestsellers': bestsellers,
        'new_products': new_products,
        'popular_left': popular_left,
        'popular_center': popular_center,
        'popular_right': popular_right
    }
    return render(request, 'sip/home.html', context)
