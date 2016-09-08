from blogapp.models import Post
from django import forms
from pagedown.widgets import PagedownWidget


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = Post
        fields = ('title', 'body', 'image','type')
