import string
from datetime import date

from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.translation import gettext_lazy as _

from orders.models import Order, OrderMessage, ThanksPage

COMMUNICATION_METHOD_CHOICES = (
        (PHONE := 'PHONE', 'Телефон'),
        (TELEGRAM := 'TELEGRAM', 'Telegram'),
        (VIBER := 'VIBER', 'Viber')
    )


class OrderForm(forms.ModelForm):
    communication_method = forms.MultipleChoiceField(
        required=False,
        choices=COMMUNICATION_METHOD_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Order

        fields = (
            'customer_name', 'phone', 'email', 'city', 'street', 'house', 'room', 'new_post_city',
            'new_post_office', 'delivery_date', 'delivery_time', 'delivery_method',
            'payment_method', 'order_note'
        )
        widgets = {
            'delivery_date': DatePickerInput(
                options={
                    'format': 'DD.MM.YYYY',
                    'locale': 'uk',
                    'minDate': date.today(),
                }
            ),
            'delivery_time': TimePickerInput(),
            'phone': forms.TextInput(attrs={'data-mask': "+38 (000) 000-00-00"})
        }
        labels = {
            'customer_name': _('ПІБ '),
            'phone': _('Телефон '),
            'email': _('Email '),
            'city': _('Місто '),
            'street': _('Вулиця '),
            'house': _('Будинок '),
            'room': _('Квартира'),
            'new_post_city': _('Виберіть місто доставки '),
            'new_post_office': _('Виберiть вiддiлення ')
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['customer_name'].widget.attrs['placeholder'] = 'ПІБ'
        self.fields['phone'].widget.attrs['placeholder'] = '+38 (0XX) XXX-XX-XX'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['city'].widget.attrs['placeholder'] = 'Місто'
        self.fields['street'].widget.attrs['placeholder'] = 'Вулиця'
        self.fields['house'].widget.attrs['placeholder'] = 'Будинок'
        self.fields['room'].widget.attrs['placeholder'] = 'Квартира'
        self.fields['order_note'].widget.attrs['placeholder'] = 'Напишіть ваші побажання'
        self.fields['new_post_city'].widget.attrs['placeholder'] = 'Почніть вводити місто доставки'
        self.fields['new_post_office'].widget.attrs['placeholder'] = 'Виберіть відділення'

        self.fields['delivery_method'].widget.attrs['class'] = 'select_option'
        self.fields['payment_method'].widget.attrs['class'] = 'select_option'
        self.fields['order_note'].widget.attrs['class'] = 'order-notes'

        self.fields['delivery_method'].widget.attrs['id'] = 'delivery-method'
        self.fields['new_post_city'].widget.attrs['id'] = 'post-city'
        self.fields['new_post_office'].widget.attrs['id'] = 'post-terminal'
        self.fields['city'].widget.attrs['id'] = 'city'
        self.fields['street'].widget.attrs['id'] = 'street'
        self.fields['house'].widget.attrs['id'] = 'house'
        self.fields['room'].widget.attrs['id'] = 'room'
        self.fields['phone'].widget.attrs['id'] = 'phone'

        self.fields['communication_method'].widget.attrs['type'] = 'checkbox'
        self.fields['phone'].widget.attrs['value'] = '+38'

        for field in self.fields:
            self.fields[field].widget.attrs['title'] = 'Заповніть це поле'

    def clean_customer_name(self):
        """Validate Order form fields"""
        customer_name = self.cleaned_data['customer_name']
        invalid_letters = string.digits + string.punctuation

        for letter in invalid_letters:
            if letter in customer_name or len(customer_name) == 1:
                raise forms.ValidationError(_('Введіть коректне ПІБ'))

        return customer_name


class OrderMessageAdminForm(forms.ModelForm):
    text_1 = forms.CharField(
        required=False,
        label=_('Текст до деталей замовлення'),
        help_text=_('Повідомлення між привітанням та деталями замовлення'),
        widget=CKEditorUploadingWidget()
    )
    text_2 = forms.CharField(
        required=False,
        label=_('Текст після деталей замовлення'),
        help_text=_('Повідомлення після деталей замовлення'),
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = OrderMessage
        fields = '__all__'


class ThanksPageAdminForm(forms.ModelForm):
    text = forms.CharField(
        required=False,
        label=_('Текст до сторінки подяки'),
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = ThanksPage
        fields = '__all__'
