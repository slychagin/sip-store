from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
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
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = 'post-comment-form'
        self.helper.attrs = {
            'novalidate': ''
        }
        self.helper.layout = Layout(
            Row(
                Column('name', ),
                Column('email')
            ),
            'content',
            FormActions(
                Submit('submit', 'Залишити коментар', css_class='comment_button', css_id='ajax_comment')
            )
        )

        for field in self.fields:
            self.fields[field].widget.attrs['title'] = 'Заповніть це поле'

    def clean_content(self):
        """Validate content field by length (not greater 1000 sings)"""
        content = self.cleaned_data['content']

        if len(content) > 1000:
            raise forms.ValidationError(_('Коментар не повинен бути більш ніж 1000 знаків.'))

        return content
