from django import forms

from orders.models import Subscribers


class SubscribeForm(forms.ModelForm):

    class Meta:
        model = Subscribers
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(SubscribeForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['placeholder'] = 'Введіть свій email'
        self.fields['email'].widget.attrs['id'] = 'mc-email'
