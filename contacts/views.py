from django.views.generic import TemplateView


class ContactsView(TemplateView):
    """Rendering contact page"""
    template_name = 'contacts/contacts.html'


