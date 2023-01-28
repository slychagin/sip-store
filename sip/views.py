from django.views.generic.base import TemplateView

from banners.models import WeekOfferBanner
from benefits.models import Benefits, Partners
from sales.models import (
    BestSellers,
    NewProducts,
    MostPopularLeft,
    MostPopularCenter,
    MostPopularRight
)


class HomePageView(TemplateView):
    """Rendering home page"""
    template_name = 'sip/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['benefits'] = Benefits.objects.all()
        context['bestsellers'] = BestSellers.objects.all()
        context['new_products'] = NewProducts.objects.all()
        context['popular_left'] = MostPopularLeft.objects.all()
        context['popular_center'] = MostPopularCenter.objects.all()
        context['popular_right'] = MostPopularRight.objects.all()
        context['partners'] = Partners.objects.all()
        context['week_offer_banners'] = WeekOfferBanner.objects.all()
        return context
