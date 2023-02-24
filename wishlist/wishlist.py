from carts.basket import Basket
from store.models import Product


class Wishlist:
    """A base Wishlist class"""
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get('wishlist')
        if 'wishlist' not in request.session:
            wishlist = self.session['wishlist'] = {}
        self.wishlist = wishlist

    def add_to_wishlist(self, product):
        """Add and update data to the session"""
        product_id = str(product.id)

        if product_id in self.wishlist:
            del self.wishlist[product_id]
        else:
            self.wishlist[product_id] = {
                'product_id': str(product.id),
            }
        self.save_session_data()

    def __iter__(self):
        """Iterate all items from wishlist"""
        product_ids = self.wishlist.keys()
        products = Product.objects.filter(id__in=product_ids)
        wishlist = self.wishlist.copy()

        for product in products:
            wishlist[str(product.id)]['product'] = product

        for item in wishlist.values():
            yield item

    def __len__(self):
        """Count the product quantity in the wishlist"""
        return sum(1 for _ in self.wishlist.keys())

    def delete_from_wishlist(self, product):
        """Delete product from wishlist"""
        product_id = str(product)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save_session_data()

    def save_session_data(self):
        """Save changes in session"""
        self.session.modified = True
