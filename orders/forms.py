from datetime import date

from django import forms

from orders.models import Order


class DateInput(forms.DateInput):
    input_type = 'date'
    initial = date.today().strftime("%Y-%m-%d")


class TimeInput(forms.TimeInput):
    input_type = 'time'


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
            'delivery_date': DateInput(),
            'delivery_time': TimeInput(),
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['customer_name'].widget.attrs['placeholder'] = 'ПІБ'
        self.fields['phone'].widget.attrs['placeholder'] = '+38 (0ХХ) ХХХ-ХХ-ХХ'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['city'].widget.attrs['placeholder'] = 'Місто'
        self.fields['street'].widget.attrs['placeholder'] = 'Вулиця'
        self.fields['house'].widget.attrs['placeholder'] = 'Будинок'
        self.fields['room'].widget.attrs['placeholder'] = 'Квартира'
        self.fields['order_note'].widget.attrs['placeholder'] = 'Напишіть ваші побажання'
        self.fields['new_post_city'].widget.attrs['placeholder'] = 'Виберіть місто доставки'
        self.fields['new_post_office'].widget.attrs['placeholder'] = 'Виберіть відділення'

        self.fields['delivery_method'].widget.attrs['class'] = 'select_option'
        self.fields['payment_method'].widget.attrs['class'] = 'select_option'
        self.fields['order_note'].widget.attrs['class'] = 'order-notes'
        self.fields['new_post_city'].widget.attrs['id'] = 'post-city'

        self.fields['new_post_city'].widget.attrs.update({'class': 'js-example-basic-single'})


        self.fields['communication_method'].widget.attrs['type'] = 'checkbox'
