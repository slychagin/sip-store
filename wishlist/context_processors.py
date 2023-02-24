from wishlist.wishlist import Wishlist


def get_wishlist(request):
    return {'wishlist': Wishlist(request)}
