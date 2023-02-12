from django.shortcuts import render


def place_order(request):
    """Rendering order page"""
    return render(request, 'orders/order.html')
