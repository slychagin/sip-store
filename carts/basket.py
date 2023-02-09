from store.models import Product


# TODO: Надо сделать, чтобы товары не отображались при переключении статуса товара в "недоступный"
class Basket:
    """A base Basket class"""

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, entered_quantity):
        """Add and update data to the session"""
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] += entered_quantity
        else:
            self.basket[product_id] = {
                'price': str(product.price),
                'qty': int(entered_quantity)
            }
        self.save_session_data()

    def __iter__(self):
        """Iterate all items from basket"""
        product_ids = [num for num in self.basket.keys() if not num.startswith('wish')]
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
        self.save_session_data()

    def subtract_quantity(self, product):
        """Decrease quantity by one after press minus button in the session data"""
        product_id = str(product)
        self.basket[product_id]['qty'] -= 1
        self.save_session_data()

    def delete(self, product):
        """Delete product from session data"""
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save_session_data()

    def save_session_data(self):
        """Save changes in session"""
        self.session.modified = True
