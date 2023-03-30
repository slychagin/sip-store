import copy

from store.models import Product


class Wishlist:
    """A base Wishlist class"""
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get('wishlist')
        if 'wishlist' not in request.session:
            wishlist = self.session['wishlist'] = {}
        self.wishlist = wishlist

    def add_wishlist(self, product):
        """Add and update data to the session after adding product"""
        product_id = str(product.id)

        if product_id not in self.wishlist:
            self.wishlist[product_id] = {
                'product_id': str(product.id),
            }
        self.save()

    def delete_wishlist(self, product_id):
        """Delete product from wishlist"""
        if str(product_id) in self.wishlist:
            del self.wishlist[str(product_id)]
        self.save()

    def __iter__(self):
        """Iterate all items from wishlist"""
        product_ids = self.wishlist.keys()
        products = Product.objects.filter(id__in=product_ids)
        wishlist = copy.deepcopy(self.wishlist)

        for product in products:
            wishlist[str(product.id)]['product'] = product

        for item in wishlist.values():
            yield item

    def __len__(self):
        """Count the product quantity in the wishlist"""
        return sum(1 for _ in self.wishlist.keys())

    def save(self):
        """Save changes in session"""
        self.session.modified = True
