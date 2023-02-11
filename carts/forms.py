from datetime import date

from django import forms

from carts.models import Coupon


class CouponAdminForm(forms.ModelForm):
    """
    Validation for entered validity coupon date in admin panel.
    Raise exception if admin entered date less than current date
    """
    class Meta:
        model = Coupon
        fields = ('coupon_kod', 'discount', 'validity', 'is_available', 'description')

    def clean(self):
        cleaned_data = super(CouponAdminForm, self).clean()
        validity_date = cleaned_data['validity']
        discount = cleaned_data['discount']
        current_date = date.today()

        if validity_date < current_date:
            raise forms.ValidationError('Введіть дату більш ніж сьогоднішня дата.')

        if discount < 1 or discount > 100:
            raise forms.ValidationError('Введіть знижку від 1 до 100 відсотків')

        return cleaned_data


