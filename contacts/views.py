from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView

from contacts.models import SalePoint


class ContactsView(TemplateView):
    """Rendering contact page"""
    template_name = 'contacts/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.GOOGLE_API_KEY
        context['sale_points'] = SalePoint.objects.filter(is_opened=True)
        return context


def map_data(request):
    """
    Get data from database about sale points (name, city,
    longitude, latitude etc.)
    """
    data_list = list(SalePoint.objects
                     .filter(is_opened=True)
                     .exclude(latitude__exact='')
                     .exclude(longitude__exact='')
                     .values())

    return JsonResponse(data_list, safe=False)
