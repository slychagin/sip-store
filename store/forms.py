from django import forms
from django.utils.translation import gettext_lazy as _

from store.models import ProductGallery, Product

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductAdminForm(forms.ModelForm):
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
    description = forms.CharField(
        required=False,
        label=_('Інформація щодо товару'),
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = Product
        fields = '__all__'


class ProductGalleryForm(forms.ModelForm):
    """Validation that prohibit to enter image and video together"""
    class Meta:
        model = ProductGallery
        fields = '__all__'

    def clean(self):
        """Rase error if administrator entered image and video"""
        cleaned_data = super(ProductGalleryForm, self).clean()
        image = cleaned_data['image']
        video = cleaned_data['video']

        if not image and not video:
            raise forms.ValidationError('Треба ввести або фото або відео!')
        if image and video:
            raise forms.ValidationError('Введіть щось одне - або фото або відео!')

        return cleaned_data
