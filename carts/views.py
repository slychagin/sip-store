from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from store.models import Product


def _cart_id(request):
    """Get the cart by session_key present in the session"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    """Add the particular product with entered quantity to the cart by product id"""
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except ObjectDoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

        entered_quantity = int(request.POST['quantity'])

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += entered_quantity
        except ObjectDoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=entered_quantity,
                cart=cart)
        cart_item.save()
        return redirect('cart')


def add_quantity(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')


def remove_cart(request, product_id):
    """Pressing the minus button decreases the quantity of product by one"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_id):
    """Delete product from cart"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart_page(request, total=0, quantity=0, cart_items=None):
    """Render the cart page"""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items
    }
    return render(request, 'store/cart.html', context)
