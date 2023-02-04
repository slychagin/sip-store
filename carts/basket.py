from django.core.exceptions import ObjectDoesNotExist

from carts.models import Cart, CartItem
from store.models import Product


class Basket:
    """A base Cart class"""

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, entered_quantity):
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] += entered_quantity
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': int(entered_quantity)}

        self.save_session_data()

    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        """Count the quantity from the basket data"""
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        """Count total sum in the basket"""
        return sum(int(item['price']) * item['qty'] for item in self.basket.values())

    def delete(self, product):
        """Delete product from session data"""
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save_session_data()

    def save_session_data(self):
        """Set session modified to true"""
        self.session.modified = True



