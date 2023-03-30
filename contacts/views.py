import json

from django.conf import settings
from crispy_forms.utils import render_crispy_form
from django.http import JsonResponse, HttpResponse
from django.template.context_processors import csrf
from django.views.generic import TemplateView

from contacts.forms import ContactForm
from contacts.models import SalePoint
from contacts.send_email import send_email_to_corporate_mail


class ContactsView(TemplateView):
    """Rendering contact page with contact form"""
    template_name = 'contacts/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact_form = ContactForm(self.request.POST or None)
        context['key'] = settings.GOOGLE_API_KEY
        context['sale_points'] = SalePoint.objects.filter(is_opened=True)
        context['form'] = contact_form
        return context

    def post(self, request, *args, **kwargs):
        """
        Check if request from ajax than check form and if is valid - send
        email to admin, if not - show errors with crispy forms
        """
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        if is_ajax:
            context = self.get_context_data(**kwargs)
            form = context['form']

            if form.is_valid():
                resp = {'success': True}
                send_email_to_corporate_mail(form)
                return HttpResponse(json.dumps(resp), content_type='application/json')
            else:
                resp = {'success': False}
                csrf_context = {}
                csrf_context.update(csrf(request))
                contact_form = render_crispy_form(form, context=csrf_context)
                resp['html'] = contact_form
            return HttpResponse(json.dumps(resp), content_type='application/json')


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
