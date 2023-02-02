from django.core.exceptions import ObjectDoesNotExist
from carts.views import _cart_id
from .models import Cart, CartItem


def cart_counter(request):
    """Count quantity of products in the cart"""
    cart_count = 0
    total_sum = 0
    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        cart_items = CartItem.objects.all().filter(cart=cart[:1])
        for cart_item in cart_items:
            cart_count += cart_item.quantity
            total_sum += cart_item.product.price * cart_item.quantity
    except ObjectDoesNotExist:
        cart_count = 0
        total_sum = 0
        cart_items = []
    return dict(cart_items=cart_items, cart_count=cart_count, total_sum=total_sum)
