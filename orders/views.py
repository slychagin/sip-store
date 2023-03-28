from datetime import datetime

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from carts.basket import Basket
from orders.forms import OrderForm
from orders.models import (
    Order,
    NewPostTerminals,
    OrderItem,
    save_customer,
    ThanksPage
)

from orders.send_email import send_email_to_customer
from store.models import count_products
from telebot.telegram import send_to_telegram_order_message


class OrderFormView(FormView):
    """Rendering Order form in the order page"""
    template_name = 'orders/order.html'
    form_class = OrderForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        basket = Basket(request)

        try:
            discount = int(basket.get_total_price() * request.session['discount'] / 100)
            total_with_discount = int(basket.get_total_price() - discount)
        except KeyError:
            discount = 0
            total_with_discount = int(basket.get_total_price())

        return render(request, self.template_name, {
            'form': form,
            'basket': basket,
            'discount': discount,
            'total_with_discount': total_with_discount
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        basket = Basket(request)

        try:
            discount = int(basket.get_total_price() * request.session['discount'] / 100)
            total_with_discount = int(basket.get_total_price() - discount)
        except KeyError:
            discount = 0
            total_with_discount = int(basket.get_total_price())

        if form.is_valid():
            order = Order()

            order.customer_name = form.cleaned_data['customer_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']

            order.city = form.cleaned_data['city']
            order.street = form.cleaned_data['street']
            order.house = form.cleaned_data['house']
            order.room = form.cleaned_data['room']

            order.new_post_city = form.cleaned_data['new_post_city']
            order.new_post_office = form.cleaned_data['new_post_office']

            order.delivery_date = form.cleaned_data['delivery_date']
            order.delivery_time = form.cleaned_data['delivery_time']

            order.delivery_method = form.cleaned_data['delivery_method']
            order.payment_method = form.cleaned_data['payment_method']
            order.communication_method = form.cleaned_data['communication_method']
            order.order_note = form.cleaned_data['order_note']
            order.ip = request.META.get('REMOTE_ADDR')
            order.is_ordered = True
            order.discount = discount
            order.order_total = total_with_discount
            order.save()

            # Generate order number
            current_date = datetime.now().strftime('%Y%m%d')
            order.order_number = current_date + '-' + str(order.pk)
            order.save()

            # Save qty to product ordered count
            count_products(basket)

            # Create order items in OrderItem model
            create_order_items(basket, order)

            # Save customer to the database
            save_customer(order)

            # Send an email with order details to the customer's email
            send_email_to_customer(basket, order)

            # Send message with order details to admin Telegram chat
            send_to_telegram_order_message(basket, order)

            # Clear basket session data
            try:
                del request.session['basket']
                del request.session['discount']
            except KeyError:
                pass

            return HttpResponseRedirect(reverse('thanks'))

        else:

            if basket.get_total_price() == 0:
                return redirect('store')

            return render(request, self.template_name, {
                'form': form,
                'discount': discount,
                'total_with_discount': total_with_discount
            })


def create_order_items(basket, order):
    """Create and save order items"""
    for item in basket.__iter__():
        ordered_product = OrderItem()

        ordered_product.order = order
        ordered_product.product = item['product']
        ordered_product.price = item['price']
        ordered_product.quantity = item['qty']
        ordered_product.is_ordered = True
        ordered_product.user_email = order.email
        ordered_product.save()


def post_city_search(request):
    """Search New Post cities input"""
    if 'term' in request.GET:
        search_string = request.GET.get('term')
        query = NewPostTerminals.objects.values('city').distinct().filter(city__istartswith=search_string)[:10]
        cities = [city['city'] for city in query]
        if cities:
            return JsonResponse(cities, safe=False)
        return JsonResponse(['Нічого не знайдено'], safe=False)


def post_terminal_search(request):
    """Search New Post terminals input"""
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

        if terminals:
            return JsonResponse(terminals, safe=False)
        return JsonResponse(['Нічого не знайдено'], safe=False)


class ThanksPageView(TemplateView):
    """Render success page after order complete"""
    template_name = 'orders/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            thanks_text = ThanksPage.objects.all()[0]
        except IndexError:
            thanks_text = ''
        context['thanks_text'] = thanks_text
        return context


