from django.shortcuts import render

from benefits.models import Benefits
from sales.models import BestSellers


def home(request):
    """Rendering home page"""
    benefits = Benefits.objects.all()
    bestsellers = BestSellers.objects.all()

    context = {
        'benefits': benefits,
        'bestsellers': bestsellers
    }
    return render(request, 'sip/home.html', context)
