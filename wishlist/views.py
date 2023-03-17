from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from store.models import Product
from wishlist.wishlist import Wishlist


class WishlistPageView(TemplateView):
    """Render Wishlist page"""
    template_name = 'store/wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist'] = Wishlist(self.request)
        return context


def add_wishlist(request):
    """Add the particular product to the wishlist by product id"""
    wishlist = Wishlist(request)
    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=product_id)

        wishlist.add_to_wishlist(product)

        wishlist_qty = wishlist.__len__()
        response = JsonResponse({'qty': wishlist_qty})
        return response


def wishlist_delete(request):
    """Delete product from the wishlist"""
    wishlist = Wishlist(request)
    if request.POST.get('action') == 'POST':
        product_id = int(request.POST.get('product_id'))

        wishlist.delete_from_wishlist(product=product_id)

        wishlist_qty = wishlist.__len__()
        response = JsonResponse({'qty': wishlist_qty})
        return response
