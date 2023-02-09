from wishlist.wishlist import Wishlist


def get_wishlist(request):
    wishlist_all = Wishlist(request)

    # Get products in wishlist without products in basket
    wishlist_filtered = [item for item in wishlist_all if 'wish_id' in item.keys()]

    return {'wishlist_all': wishlist_all, 'wishlist_filtered': wishlist_filtered}
