from django.core.exceptions import ObjectDoesNotExist


from .basket import Basket
from .models import Cart, CartItem


# def get_mini_cart_data(request):
#     """Count quantity of products in the cart"""
#     cart_count = 0
#     total_sum = 0
#     cart = Basket(request)
#     try:
#         cart = Cart.objects.filter(cart_id=cart.basket)
#         cart_items = CartItem.objects.all().filter(cart=cart[:1])
#         for cart_item in cart_items:
#             cart_count += cart_item.quantity
#             total_sum += cart_item.product.price * cart_item.quantity
#     except ObjectDoesNotExist:
#         cart_count = 0
#         total_sum = 0
#         cart_items = []
#     return dict(cart_items=cart_items, cart_count=cart_count, total_sum=total_sum)


def basket(request):
    return {'basket': Basket(request)}
