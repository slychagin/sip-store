from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    """Create contact form in the contacts page"""
    name = forms.CharField(max_length=100, label=_("Ім'я"))
    email = forms.EmailField(max_length=100, label=_('Електронна пошта'))
    title = forms.CharField(max_length=200, label=_('Тема'))
    message = forms.CharField(widget=forms.Textarea(), label=_('Повідомлення'))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = _("Введіть Ваше ім'я")
        self.fields['email'].widget.attrs['placeholder'] = _('Введіть Вашу електронну пошту')
        self.fields['title'].widget.attrs['placeholder'] = _('Введіть тему повідомлення')
        self.fields['message'].widget.attrs['placeholder'] = _('Текст повідомлення')

        for field in self.fields:
            self.fields[field].widget.attrs['title'] = _('Заповніть це поле')

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = 'contact-form'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            'name',
            'email',
            'title',
            'message',
            FormActions(
                Submit('submit', 'Відправити', css_class='contact_button', css_id='ajax_contact')
            )
        )

    def clean_message(self):
        """Validate message field by length (not greater 2000 sings)"""
        message = self.cleaned_data['message']

        if len(message) > 2000:
            raise forms.ValidationError(_('Повідомлення не повинно бути більш ніж 2000 знаків.'))

        return message
