from .basket import Basket


def cart(request):
    basket_all = Basket(request)

    # Get products in basket without products in wishlist
    basket_filtered = [item for item in basket_all if 'wish_id' not in item.keys()]

    return {'basket_all': basket_all, 'basket_filtered': basket_filtered}
