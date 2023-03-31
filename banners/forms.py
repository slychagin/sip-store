from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.translation import gettext_lazy as _

from banners.models import MainBanner


class MainBannerAdminForm(forms.ModelForm):
    """Connect content title and description fields to CKEditor"""
    title = forms.CharField(label=_('Заголовок'), widget=CKEditorUploadingWidget())
    description = forms.CharField(label=_('Опис'), widget=CKEditorUploadingWidget())

    class Meta:
        model = MainBanner
        fields = '__all__'
