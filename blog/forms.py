from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from blog.models import Post, PostComment


class PostAdminForm(forms.ModelForm):
    """Connect content field to CKEditor"""
    description = forms.CharField(
        label=_('Контент'),
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = Post
        fields = '__all__'


class PostCommentForm(forms.ModelForm):
    """Create a new comment form"""

    class Meta:
        model = PostComment
        fields = ('name', 'email', 'content')
        labels = {
            'name': _("Ім'я"),
            'email': _('Email'),
            'content': _('Коментар')
        }
        widgets = {
            'content': Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(PostCommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['title'] = 'Заповніть це поле'

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_id = 'post-comment-form'
        self.helper.attrs = {'novalidate': ''}
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

    def clean_content(self):
        """Validate content field by length (not greater 1000 sings)"""
        content = self.cleaned_data['content']

        if len(content) > 1000:
            raise forms.ValidationError(_('Коментар не повинен бути більш ніж 1000 знаків.'))

        return content


class PostCommentAdminForm(forms.ModelForm):
    """Create comment form in admin panel"""

    class Meta:
        model = PostComment
        fields = '__all__'

    def clean(self):
        """
        Rase error if administrator entered comment for post
        in admin panel with not unique email
        """
        cleaned_data = super(PostCommentAdminForm, self).clean()
        email = cleaned_data['email']
        post = cleaned_data['post']

        email_list = [post.email for post in PostComment.objects.filter(post=post)]

        if email in email_list and self.instance.pk is None:
            raise forms.ValidationError('Коментар з таким email до даного посту вже існує.')

        return cleaned_data
