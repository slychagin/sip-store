from django.shortcuts import render

from banners.models import WeekOfferBanner
from benefits.models import Benefits, Partners
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
    partners = Partners.objects.all()
    week_offer_banners = WeekOfferBanner.objects.all()

    context = {
        'benefits': benefits,
        'bestsellers': bestsellers,
        'new_products': new_products,
        'popular_left': popular_left,
        'popular_center': popular_center,
        'popular_right': popular_right,
        'partners': partners,
        'week_offer_banners': week_offer_banners
    }
    return render(request, 'sip/home.html', context)
