from django.shortcuts import render
from benefits.models import Benefits


def home(request):
    """Rendering home page"""
    benefits = Benefits.objects.all()

    context = {
        'benefits': benefits
    }
    return render(request, 'sip/home.html', context)
