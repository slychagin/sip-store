from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from banners.models import (
    WeekOfferBanner,
    MainBanner,
    TwoBanners,
    OfferSingleBanner,
    FooterBanner
)
from benefits.models import Benefits, Partners
from orders.models import Subscribers
from sales.models import (
    BestSellers,
    NewProducts,
    MostPopularLeft,
    MostPopularCenter,
    MostPopularRight
)
from store.models import Product, ProductGallery


class HomePageView(TemplateView):
    """Rendering home page"""
    template_name = 'sip/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['benefits'] = Benefits.objects.all()
        context['bestsellers'] = BestSellers.objects.\
            filter(product_1__is_available=True).\
            filter(product_2__is_available=True)
        context['new_products'] = NewProducts.objects.\
            filter(product_1__is_available=True).\
            filter(product_2__is_available=True)
        context['popular_left'] = MostPopularLeft.objects.\
            filter(product_1__is_available=True).\
            filter(product_2__is_available=True).\
            filter(product_3__is_available=True)
        context['popular_center'] = MostPopularCenter.objects.\
            filter(product_1__is_available=True).\
            filter(product_2__is_available=True).\
            filter(product_3__is_available=True)
        context['popular_right'] = MostPopularRight.objects.\
            filter(product_1__is_available=True).\
            filter(product_2__is_available=True).\
            filter(product_3__is_available=True)
        context['partners'] = Partners.objects.all()
        context['week_offer_banners'] = WeekOfferBanner.objects.\
            filter(product__is_available=True)
        context['main_banner'] = MainBanner.objects.all()
        context['two_banners'] = TwoBanners.objects.all()
        context['offer_single_banner'] = OfferSingleBanner.objects.all()
        context['footer_banner'] = FooterBanner.objects.all()
        return context


def get_single_product(request):
    """Return single product data by id to use in product quick show"""
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        product = Product.objects.get(id=product_id)

        # Get all images and videos from Product Gallery
        product_gallery = ProductGallery.objects.filter(product=product)
        images = [i.image.url for i in product_gallery if i.image != '']
        videos = [i.video for i in product_gallery if i.video != '']

        data = {
            'title': product.product_name,
            'price': product.price,
            'old_price': product.price_old,
            'description': product.short_description,
            'image_main': product.product_image.url,
            'product_url': product.get_url(),
            'unit': product.unit
        }

        for num, img in enumerate(images):
            data[f'img{num + 1}'] = img

        if videos:
            for num, video in enumerate(videos):
                data[f'video{num + 1}'] = video
            data['target'] = '_blank'
        else:
            data[f'video1'] = product.get_url()
            data['target'] = '_self'

        response = JsonResponse(data=data)

        return response


def subscribe(request):
    """Subscribe the user in subscribe form"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            validate_email(email)
        except ValidationError:
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
