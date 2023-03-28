from importlib import import_module
from urllib.parse import urlencode

from django.conf import settings
from django.test import override_settings
from django.test import (
    TestCase,
    Client,
    RequestFactory
)
from django.urls import reverse

from contacts.forms import ContactForm
from contacts.models import SalePoint
from contacts.views import ContactsView


class ContactsViewTest(TestCase):
    """Tests ContactsView"""

    @classmethod
    def setUpTestData(cls):
        """Create sale point object"""
        SalePoint.objects.create(name='Sale point 1')
        SalePoint.objects.create(name='Sale point 2')

    def setUp(self):
        """Create view, client and request"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = ContactsView()

    def test_contacts_view_url_exists_at_desired_location(self):
        """Tests that contacts view url exists at desired location"""
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_contacts_view_url_accessible_by_name(self):
        """Tests contacts view url accessible by name"""
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_view_uses_correct_template(self):
        """Tests contacts view uses correct template"""
        response = self.client.get(reverse('contacts'))
        self.assertTemplateUsed(response, 'contacts/contacts.html')

    def test_contacts_page_html(self):
        """Test Contacts html"""
        request = self.factory.get('/contacts/')
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        self.view.setup(request)
        response = self.view.dispatch(request)
        html = response.render().content.decode('utf-8')

        self.assertIn('Наші контакти', html)
        self.assertIn('Повідомлення', html)
        self.assertTrue(html.startswith('\n\n<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_view_context(self):
        """Tests ContactsView context"""
        request = self.factory.get('/contacts/')
        self.view.setup(request)
        context = self.view.get_context_data()

        self.assertEqual(context['key'], settings.GOOGLE_API_KEY)
        self.assertTrue(len(context['sale_points']) == 2)
        self.assertTrue(isinstance(context['form'], ContactForm))

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_contacts_view_post_method_with_valid_form(self):
        """Tests post method. Check contacts form."""
        data = {
            'name': 'Serhio',
            'email': 'email@gmail.com',
            'title': 'Hello!',
            'message': 'Post message'
        }

        response = self.client.post(
            reverse('contacts'),
            data=urlencode(data),
            xhr=True,
            content_type='application/x-www-form-urlencoded',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
    def test_contacts_view_post_method_with_invalid_form(self):
        """Tests post method. Check contacts form."""
        data = {
            'name': 'Serhio',
            'email': 'email@gmail.com',
            'title': 'Hello!',
            'message': ''
        }

        response = self.client.post(
            reverse('contacts'),
            data=urlencode(data),
            xhr=True,
            content_type='application/x-www-form-urlencoded',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertFormError(response, 'form', 'message', "Це поле обов'язкове.")


class MapDataTest(TestCase):
    """Tests data from database about sale points"""

    @classmethod
    def setUpTestData(cls):
        """Create sale point objects"""
        cls.sale_point_1 = SalePoint.objects.create(
            name='Sale point 1', latitude='23.0152', longitude='35.1234'
        )
        cls.sale_point_2 = SalePoint.objects.create(
            name='Sale point 2', latitude='23.0152', longitude='35.1234', is_opened=False
        )
        cls.sale_point_3 = SalePoint.objects.create(
            name='Sale point 3', is_opened=True
        )

    def setUp(self):
        """Create view, client and request"""
        self.client = Client()
        self.factory = RequestFactory()
        self.view = ContactsView()

    def test_map_data(self):
        """
        Tests that map data function get just data with not empty
        longitude and latitude and with status is_opened is True
        """
        response = self.client.get(reverse('map_data'))
        response_values = response.json()[0].values()

        self.assertEqual(len(response.json()), 1)
        self.assertNotIn(str(self.sale_point_2), response_values)
        self.assertNotIn(str(self.sale_point_3), response_values)
