from django.shortcuts import render


def wishlist_page(request):
    """Render Wishlist page"""
    return render(request, 'store/wishlist.html')
