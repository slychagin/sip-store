from .basket import Basket


def cart(request):
    return {'basket': Basket(request)}
