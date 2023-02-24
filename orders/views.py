import json
from datetime import datetime

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView

from carts.basket import Basket
from orders.forms import OrderForm

# TODO: Сделать, чтобы сумма и скидка в заказе повторяла корзину после обновления.
from orders.models import Order, NewPostTerminals


class OrderFormView(View):
    """Rendering Order form in the order page"""
    template_name = 'orders/order.html'
    form_class = OrderForm
    discount = 0
    total_with_discount = 0

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        basket = Basket(request)
        basket_filtered = [item for item in basket if 'wish_id' not in item.keys()]
        try:
            discount = int(basket.get_total_price() * basket_filtered[0]['discount'] / 100)
            total_with_discount = int(basket.get_total_price() - discount)
        except KeyError:
            discount = 0
            total_with_discount = int(basket.get_total_price())
        except IndexError:
            return redirect('cart')

        return render(request, self.template_name, {
            'form': form,
            'order': Order,
            'basket': basket_filtered,
            'discount': discount,
            'total_with_discount': total_with_discount
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        # get delivery methods
        courier = Order.DELIVERY_METHOD_CHOICES[0][0]
        delivery_company = Order.DELIVERY_METHOD_CHOICES[1][0]

        if request.POST.get('action') == 'POST':
            delivery_method = request.POST.get('delivery_method')
            # request.session['delivery_method'] = delivery_method
            print(delivery_method)

            if delivery_method == courier:
                form.fields['city'].required = True
                form.fields['street'].required = True
                form.fields['house'].required = True
                form.fields['new_post_city'].required = False
                form.fields['new_post_office'].required = False
            if delivery_method == delivery_company:
                form.fields['city'].required = False
                form.fields['street'].required = False
                form.fields['house'].required = False
                form.fields['new_post_city'].required = True
                form.fields['new_post_office'].required = True


        if form.is_valid():
            data = Order()

            data.customer_name = form.cleaned_data['customer_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']

            data.city = form.cleaned_data['city']
            data.street = form.cleaned_data['street']
            data.house = form.cleaned_data['house']
            data.room = form.cleaned_data['room']

            data.new_post_city = form.cleaned_data['new_post_city']
            data.new_post_office = form.cleaned_data['new_post_office']

            data.delivery_date = form.cleaned_data['delivery_date']
            data.delivery_time = form.cleaned_data['delivery_time']
            data.delivery_method = form.cleaned_data['delivery_method']
            data.payment_method = form.cleaned_data['payment_method']
            data.communication_method = form.cleaned_data['communication_method']
            data.order_note = form.cleaned_data['order_note']
            data.ip = request.META.get('REMOTE_ADDR')
            data.is_ordered = True
            data.discount = self.discount
            data.order_total = self.total_with_discount
            data.save()

            # Generate order number
            current_date = datetime.now().strftime('%Y%m%d')
            data.order_number = current_date + '-' + str(data.pk)
            data.save()

            return HttpResponse('SUCCESS !!!')
        return render(request, self.template_name, {'form': form})


def post_city_search(request):
    """Search new post cities input"""
    if 'term' in request.GET:
        search_string = request.GET.get('term')
        query = NewPostTerminals.objects.values('city').distinct().filter(city__istartswith=search_string)[:10]
        cities = [city['city'] for city in query]
        if cities:
            return JsonResponse(cities, safe=False)
        return JsonResponse(['Нічого не знайдено'], safe=False)


def post_terminal_search(request):
    """Search new post terminals input"""
    if request.POST.get('action') == 'POST':
        city_name = request.POST.get('city_name')
        request.session['city'] = city_name
        response = JsonResponse({'city_name': city_name})
        return response

    if 'term' in request.GET:
        try:
            city = request.session['city']
        except KeyError:
            return JsonResponse(['Оберіть спочатку місто доставки'], safe=False)

        search_string = request.GET.get('term')
        query = NewPostTerminals.objects.filter(city=city).values('terminal').filter(terminal__icontains=search_string)
        terminals = [terminal['terminal'] for terminal in query]

        try:
            del request.session['city']
        except KeyError:
            return JsonResponse(['Оберіть спочатку місто доставки'], safe=False)

        if terminals:
            return JsonResponse(terminals, safe=False)
        return JsonResponse(['Нічого не знайдено'], safe=False)
