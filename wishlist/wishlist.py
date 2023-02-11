from carts.basket import Basket
from store.models import Product


class Wishlist(Basket):
    """A base Wishlist class"""
    def __init__(self, request):
        super().__init__(request)

    def add_to_wishlist(self, product):
        """Add and update data to the session"""
        wishlist_id = f'wish{product.id}'

        if wishlist_id in self.basket:
            del self.basket[wishlist_id]
        else:
            self.basket[wishlist_id] = {
                'wish_id': str(product.id),
                'price': 0,
                'qty': 0
            }
        self.save_session_data()

    def __iter__(self):
        """Iterate all items from wishlist"""
        product_ids = [int(num[4:]) for num in self.basket.keys() if num.startswith('wish')]
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[f'wish{product.id}']['product'] = product

        for item in basket.values():
            item['price'] = int(item['price'])
            yield item

    def __len__(self):
        """Count the product quantity in the wishlist"""
        return sum(1 for item in self.basket.keys() if item.startswith('wish'))

    def delete_from_wishlist(self, product):
        """Delete product from wishlist"""
        product_id = f'wish{product}'
        if product_id in self.basket:
            del self.basket[product_id]
            self.save_session_data()
