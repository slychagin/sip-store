from wishlist.wishlist import Wishlist


def get_wishlist(request):
    wish_products_ids = [int(i['product_id']) for i in Wishlist(request)]
    return {'wishlist': Wishlist(request), 'wish_products': wish_products_ids}
