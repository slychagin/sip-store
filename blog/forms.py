from django import forms

from blog.models import Post

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    description = forms.CharField(
        label='Контент',
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = Post
        fields = '__all__'
