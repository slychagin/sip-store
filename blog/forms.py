from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.utils.translation import gettext_lazy as _

from blog.models import Post, PostComment

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    description = forms.CharField(
        label='Контент',
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentForm(forms.ModelForm):
    """Create a new comment form"""

    class Meta:
        model = PostComment
        fields = ('name', 'email', 'content')
        labels = {
            'name': _("Ім'я"),
            'email': _('Email'),
            'content': _('Коментар')
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['id'] = 'name'
        self.fields['email'].widget.attrs['id'] = 'email'
        self.fields['content'].widget.attrs['id'] = 'content'

        for field in self.fields:
            self.fields[field].widget.attrs['title'] = 'Заповніть це поле'
