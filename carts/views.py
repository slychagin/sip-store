from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from carts.basket import Basket
from carts.models import Coupon
from store.models import Product


class CartPageView(TemplateView):
    """Render Cart page"""
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket'] = Basket(self.request)
        return context


def add_cart(request):
    """
    Add the particular product with entered
    quantity to the cart by product id
    """
    basket = Basket(request)
    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        entered_quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, id=product_id)

        basket.add(product, entered_quantity)

        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty})
        return response


def plus_quantity(request):
    """Increase quantity by one after press plus button"""
    basket = Basket(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        basket.add_quantity(product_id)

        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        item_quantity = basket.get_item_quantity(product_id)
        item_total_price = basket.get_sub_total(product_id)

        response = JsonResponse({
            'qty': basket_qty,
            'total': basket_total,
            'item_qty': item_quantity,
            'item_total_price': item_total_price
        })
        return response


def minus_quantity(request):
    """Decrease quantity by one after press minus button"""
    basket = Basket(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        basket.subtract_quantity(product_id)

        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        item_quantity = basket.get_item_quantity(product_id)
        item_total_price = basket.get_sub_total(product_id)

        if item_quantity < 1:
            basket.delete(product_id)

        response = JsonResponse({
            'qty': basket_qty,
            'total': basket_total,
            'item_qty': item_quantity,
            'item_total_price': item_total_price
        })
        return response


def cart_delete(request):
    """Delete product from the cart"""
    basket = Basket(request)
    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product_id)
        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'total': basket_total})
        return response


def mini_cart_delete(request):
    """Delete product from the mini cart popup menu"""
    basket = Basket(request)
    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product_id)
        basket_qty = basket.__len__()
        mini_cart_total = basket.get_total_price()
        response = JsonResponse({
            'qty': basket_qty,
            'mini_cart_total': mini_cart_total
        })
        return response


def get_coupon(request):
    """Check coupon in database and apply discount"""
    basket = Basket(request)
    if request.POST.get('action') == 'POST':
        coupon = request.POST.get('coupon').lower()
        coupons = Coupon.objects.filter(is_available=True)
        coupons_list = [item.coupon_kod.lower() for item in coupons]
        basket_total = basket.get_total_price()

        if coupon in coupons_list:
            coupon_discount = Coupon.objects.get(coupon_kod__iexact=coupon).discount
            cart_discount = int(coupon_discount * basket_total / 100)
            total = basket_total - cart_discount
            basket.set_discount(coupon_discount)

            response = JsonResponse({
                'cart_discount': cart_discount,
                'total': total,
                'coupon_discount': coupon_discount
            })
        else:
            basket.set_discount()
            response = JsonResponse({
                'cart_discount': 0,
                'total': basket_total,
            })
        return response
