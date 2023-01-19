from django.shortcuts import render


def home(request):
    """Rendering home page"""
    return render(request, 'sip/home.html')
