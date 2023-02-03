from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView

from carts.models import Cart, CartItem
from store.models import Product


class CartListView(ListView):
    """Render the cart page"""
    template_name = 'store/cart.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = 0
        self.quantity = 0
        self.cart_items = None

    def get_queryset(self):
        """Return products added to the cart"""
        try:
            cart = Cart.objects.get(cart_id=_cart_id(self.request))
            self.cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            for cart_item in self.cart_items:
                self.total += cart_item.product.price * cart_item.quantity
                self.quantity += cart_item.quantity
        except ObjectDoesNotExist:
            pass
        return self.cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.total
        context['quantity'] = self.quantity
        context['cart_items'] = self.cart_items
        return context


def _cart_id(request):
    """Get the cart by session_key present in the session"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    """Add the particular product with entered quantity to the cart by product id"""
    # TODO: Настроить всплывающее сообщение или открытие мини корзины при добавлении товара в корзину либо

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
        return redirect('product_details', product.category.slug, product.slug)


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
