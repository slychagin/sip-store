from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from carts.basket import Basket
from carts.models import Coupon
from store.models import Product


# TODO: Переместить скрипты в отдельный файл
# TODO: Если файлы находятся в корзине и при этом обновились цены, то сумма не пересчитывается по новым ценам
def cart_page(request):
    """Render Cart page"""
    basket = Basket(request)

    # Get products in basket without products in wishlist
    basket_filtered = [item for item in basket if 'wish_id' not in item.keys()]

    context = {
        'basket': basket_filtered
    }
    return render(request, 'store/cart.html', context)


def add_cart(request):
    """Add the particular product with entered quantity to the cart by product id"""
    # TODO: Настроить всплывающее сообщение или открытие мини корзины при добавлении товара в корзину либо
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
    # TODO: Сделать ограничение по количеству (не более 99)
    # TODO: Проблема с отображением знака гривны
    basket = Basket(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        basket.add_quantity(product=product_id)

        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        item_quantity = basket.get_item_quantity(product=product_id)
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
        basket.subtract_quantity(product=product_id)

        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        item_quantity = basket.get_item_quantity(product=product_id)
        item_total_price = basket.get_sub_total(product_id)

        if item_quantity < 1:
            basket.delete(product=product_id)

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
        basket.delete(product=product_id)
        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'total': basket_total})
        return response


def mini_cart_delete(request):
    """Delete product from the mini cart popup menu"""
    # TODO: Проблема с отображением знака гривны
    basket = Basket(request)
    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product=product_id)
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
        print(coupons)
        coupons_list = [item.coupon_kod.lower() for item in coupons]
        basket_total = basket.get_total_price()

        if coupon in coupons_list:
            coupon_discount = Coupon.objects.get(coupon_kod__iexact=coupon).discount
            cart_discount = int(coupon_discount * basket_total / 100)
            total = basket_total - cart_discount

            response = JsonResponse({
                'cart_discount': cart_discount,
                'total': total
            })
        else:
            # TODO: Вывести сообщение об отсутствии такого купона
            response = JsonResponse({
                'cart_discount': 0,
                'total': basket_total
            })

        return response
