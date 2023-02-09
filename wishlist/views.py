from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from store.models import Product
from wishlist.wishlist import Wishlist


def wishlist_page(request):
    """Render Wishlist page"""
    wishlist = Wishlist(request)

    # Get products in wishlist without products in basket
    wishlist_filtered = [item for item in wishlist if 'wish_id' in item.keys()]
    print(wishlist_filtered)

    context = {
        'wishlist': wishlist_filtered
    }
    return render(request, 'store/wishlist.html', context)


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
