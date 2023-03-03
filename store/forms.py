from django import forms

from store.models import ProductGallery


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
