from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Row,
    Column,
    Submit,
    Field
)

from django import forms
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from store.models import (
    ProductGallery,
    Product,
    ReviewRating
)

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
    """Add CKEditor widget"""
    short_description = forms.CharField(
        required=False,
        label=_('Короткий опис'),
        widget=CKEditorUploadingWidget()
    )
    description = forms.CharField(
        required=False,
        label=_('Детальний опис'),
        widget=CKEditorUploadingWidget()
    )
    specification = forms.CharField(
        required=False,
        label=_('Специфікація'),
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = Product
        fields = '__all__'


class ProductInfoAdminForm(forms.ModelForm):
    """Add CKEditor widget"""
    description = forms.CharField(
        required=False,
        label=_('Інформація щодо товару'),
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = Product
        fields = '__all__'


class ProductGalleryForm(forms.ModelForm):
    """
    Validation that prohibit to enter image and video together
    """
    class Meta:
        model = ProductGallery
        fields = '__all__'

    def clean(self):
        """
        Rase error if administrator entered image and video together
        or not entered both
        """
        cleaned_data = super(ProductGalleryForm, self).clean()
        image = cleaned_data['image']
        video = cleaned_data['video']

        if not image and not video:
            raise forms.ValidationError(_('Треба ввести або фото або відео!'))
        if image and video:
            raise forms.ValidationError(_('Введіть щось одне - або фото або відео!'))

        return cleaned_data


class ReviewRatingForm(forms.ModelForm):
    """Create a new review rating form"""

    class Meta:
        model = ReviewRating
        fields = ('rating', 'review', 'name', 'email')
        labels = {
            'review': _('Ваш відгук'),
            'name': _("Ім'я"),
            'email': _('Email')
        }
        widgets = {
            'review': Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewRatingForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['title'] = 'Заповніть це поле'

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = 'review-rating-form'
        self.helper.attrs = {'novalidate': ''}
        self.helper.layout = Layout(
            Field('rating', type='hidden', id='rating'),
            'review',
            Row(
                Column('name', ),
                Column('email')
            ),
            FormActions(
                Submit('submit', 'відправити', css_class='comment_button review_button', css_id='ajax_review')
            )
        )

    def clean_rating(self):
        """Validate rating field (rating can't be < 0)"""
        rating = self.cleaned_data['rating']

        if rating == 0:
            raise forms.ValidationError(_('Будь ласка, встановіть рейтинг'))

        return rating


class ReviewRatingAdminForm(forms.ModelForm):
    """Check unique review rating by email"""

    class Meta:
        model = ReviewRating
        fields = '__all__'

    def clean(self):
        """Rase error if administrator entered review for product
        in admin panel with not unique email
        """
        cleaned_data = super(ReviewRatingAdminForm, self).clean()
        email = cleaned_data['email']
        product = cleaned_data['product']

        email_list = [review.email for review in ReviewRating.objects.filter(product=product)]

        if email in email_list and self.instance.pk is None:
            raise forms.ValidationError(_('Відгук з таким email по даному товару вже існує.'))

        return cleaned_data


class ProductsSortForm(forms.Form):
    """
    Create form with select widget for sorting
    products by selected option in the Store page
    """
    CHOICES = (
        ('id', _('сортувати')),
        ('pk', _('за замовчуванням')),
        ('-count_orders', _('за популярністю')),
        ('rating', _('за рейтингом')),
        ('price', _('від дешевих до дорогих')),
        ('-price', _('від дорогих до дешевих'))
    )
    ordering = forms.ChoiceField(choices=CHOICES, label='')

    def __init__(self, *args, **kwargs):
        super(ProductsSortForm, self).__init__(*args, **kwargs)
        self.fields['ordering'].widget.attrs['class'] = 'select_option'
        self.fields['ordering'].widget.attrs['onchange'] = 'this.form.submit()'
