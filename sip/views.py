from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from banners.models import WeekOfferBanner
from benefits.models import Benefits, Partners
from orders.models import Subscribers
from sales.models import (
    BestSellers,
    NewProducts,
    MostPopularLeft,
    MostPopularCenter,
    MostPopularRight
)
from store.models import Product


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


def get_single_product(request):
    """Return single product data by id to use in product quick show"""
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product = Product.objects.get(id=product_id)

        response = JsonResponse({
            'title': product.product_name,
            'price': product.price,
            'old_price': product.price_old,
            'description': product.description,
            'image': product.product_image.url
        })
        return response


def subscribe(request):
    """Subscribe the user in subscribe form"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            validate_email(email)
        except ValidationError as e:
            response = JsonResponse({'error': 'Введіть коректну email адресу'})
            return response
        else:
            subscriber = Subscribers.objects.filter(email=email).exists()
            if not subscriber:
                data = Subscribers()
                data.email = email
                data.save()
                response = JsonResponse({'success': 'Ви підписані!'})
                return response
