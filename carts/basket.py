import copy

from django.shortcuts import get_object_or_404

from store.models import Product


class Basket:
    """A base Basket class"""

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('basket')
        if 'basket' not in request.session:
            basket = self.session['basket'] = {}
        self.basket = basket

        # Update prices in case they have changed
        products = [get_object_or_404(Product, id=item) for item in self.basket]
        for product in products:
            self.basket[str(product.id)]['price'] = product.price

    def add(self, product, entered_quantity):
        """Add and update data to the session"""
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['price'] = str(product.price)
            self.basket[product_id]['qty'] += entered_quantity
        else:
            self.basket[product_id] = {
                'price': str(product.price),
                'qty': int(entered_quantity)
            }
        self.save()

    def __iter__(self):
        """Iterate all items from basket"""
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = copy.deepcopy(self.basket)

        for product in products:
            basket[str(product.id)]['product'] = product
            basket[str(product.id)]['price'] = product.price

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

    def set_discount(self, discount=0):
        """Saves the discount if a coupon has been applied"""
        self.session['discount'] = int(discount)

    def get_item_quantity(self, product):
        """Get quantity of current item by product id"""
        product_id = str(product)
        item_qty = self.basket[product_id]['qty']
        return item_qty

    def get_sub_total(self, product):
        """Get total price of current item"""
        product_id = str(product)
        item_qty = int(self.basket[product_id]['qty'])
        item_sub_total = int(self.basket[product_id]['price'])
        sub_total = item_qty * item_sub_total
        return sub_total

    def add_quantity(self, product):
        """Increase quantity by one after press plus button in the session data"""
        product_id = str(product)
        self.basket[product_id]['qty'] += 1
        self.save()

    def subtract_quantity(self, product):
        """Decrease quantity by one after press minus button in the session data"""
        product_id = str(product)
        self.basket[product_id]['qty'] -= 1
        self.save()

    def delete(self, product):
        """Delete product from session data"""
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def save(self):
        """Save changes in session"""
        self.session.modified = True
