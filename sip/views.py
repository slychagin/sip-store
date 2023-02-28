from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from banners.models import WeekOfferBanner
from benefits.models import Benefits, Partners
from orders.models import Subscribers
from sales.forms import SubscribeForm
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
    # TODO: Сделать всплывающее сообщение о том, что товар добавлен в корзину, в лист желаний и т.д.
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
    # TODO: Всплывающие сообщения
    if request.method == 'POST':
        form = SubscribeForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber = Subscribers.objects.filter(email=email).exists()
            if not subscriber:
                data = Subscribers()
                data.email = email
                data.save()
            messages.success(request, 'Ви підписані!')
            return redirect('home')
        else:
            messages.error(request, 'Введіть правильну email адресу.')
            return redirect('home')



