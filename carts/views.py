import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView

from carts.basket import Basket
from carts.models import Cart, CartItem
from store.models import Product


# class CartListView(ListView):
#     """Render the cart page"""
#     template_name = 'store/cart.html'
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.total = 0
#         self.quantity = 0
#         self.cart_items = None
#
#     def get_queryset(self):
#         """Return products added to the cart"""
#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(self.request))
#             self.cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#             for cart_item in self.cart_items:
#                 self.total += cart_item.product.price * cart_item.quantity
#                 self.quantity += cart_item.quantity
#         except ObjectDoesNotExist:
#             pass
#         return self.cart_items
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['total'] = self.total
#         context['quantity'] = self.quantity
#         context['cart_items'] = self.cart_items
#         return context

# def _cart_id(request):
#     """Get the cart by session_key present in the session"""
#     cart = request.session.session_key
#     if not cart:
#         cart = request.session.create()
#     return cart


def cart_page(request):
    basket = Basket(request)
    context = {
        'basket': basket
    }
    return render(request, 'store/cart.html', context)


def add_cart(request):
    """Add the particular product with entered quantity to the cart by product id"""
    # TODO: Настроить всплывающее сообщение или открытие мини корзины при добавлении товара в корзину либо
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        entered_quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, id=product_id)

        basket.add(product, entered_quantity)

        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty})



        # try:
        #     cart = Cart.objects.get(cart_id=basket.basket)
        # except ObjectDoesNotExist:
        #     cart = Cart.objects.create(cart_id=basket.basket)
        #     cart.save()
        #
        # try:
        #     cart_item = CartItem.objects.get(product=product, cart=cart)
        #     cart_item.quantity += entered_quantity
        # except ObjectDoesNotExist:
        #     cart_item = CartItem.objects.create(
        #         product=product,
        #         quantity=entered_quantity,
        #         cart=cart)
        # cart_item.save()



        return response



# def add_cart(request):
#     """Add the particular product with entered quantity to the cart by product id"""
#     # TODO: Настроить всплывающее сообщение или открытие мини корзины при добавлении товара в корзину либо
#
#     if request.POST.get('action') == 'post':
#         product_id = int(request.POST.get('product_id'))
#         entered_quantity = int(request.POST.get('quantity'))
#         product = Product.objects.get(id=product_id)
#
#         try:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#         except ObjectDoesNotExist:
#             cart = Cart.objects.create(cart_id=_cart_id(request))
#             cart.save()
#
#         try:
#             cart_item = CartItem.objects.get(product=product, cart=cart)
#             cart_item.quantity += entered_quantity
#         except ObjectDoesNotExist:
#             cart_item = CartItem.objects.create(
#                 product=product,
#                 quantity=entered_quantity,
#                 cart=cart)
#         cart_item.save()
#         response = JsonResponse({'total_quantity': cart_item.quantity})
#         print(json.loads(response.content)['total_quantity'])
#         return response


def plus_quantity(request):
    """Increase quantity by one after press plus button"""
    # TODO: Сделать ограничение по количеству (не более 99)
    basket = Basket(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        basket.add_quantity(product=product_id)

        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        item_quantity = basket.get_item_quantity(product=product_id)
        item_total_price = basket.get_sub_total(product_id)

        # product = Product.objects.get(id=product_id)
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        # cart_item = CartItem.objects.get(product=product, cart=cart)
        # cart_item.quantity += 1
        # cart_item.save()
        response = JsonResponse({
            'qty': basket_qty,
            'total': f'{basket_total} ₴',
            'item_qty': item_quantity,
            'item_total_price': f'{item_total_price} ₴'
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

        #     cart = Cart.objects.get(cart_id=_cart_id(request))
        #     product = get_object_or_404(Product, id=product_id)
        #     cart_item = CartItem.objects.get(product=product, cart=cart)
        #     if cart_item.quantity > 1:
        #         cart_item.quantity -= 1
        #         cart_item.save()
        #     else:
        #         cart_item.delete()
        #     return redirect('cart')

        response = JsonResponse({
            'qty': basket_qty,
            'total': f'{basket_total} ₴',
            'item_qty': item_quantity,
            'item_total_price': f'{item_total_price} ₴'
        })
        return response


def cart_delete(request):
    """Delete product from cart"""
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product=product_id)
        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'total': basket_total})
        return response

    # cart = Cart.objects.get(cart_id=_cart_id(request))
    # product = get_object_or_404(Product, id=product_id)
    # cart_item = CartItem.objects.get(product=product, cart=cart)
    # cart_item.delete()
    # return redirect('cart')
