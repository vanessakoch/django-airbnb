from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Post, PostComment

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.add_input(Submit('submit', 'Postar', css_class='btn-salvar'))

class CommentForm(forms.ModelForm):

    class Meta:
        model = PostComment
        fields = ('author', 'text',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.attrs = {'novalidate': ''}
        self.helper.add_input(Submit('submit', 'Comentar', css_class='btn-salvar'))