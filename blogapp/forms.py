from blogapp.models import Post, User
from django import forms
from pagedown.widgets import PagedownWidget
from django.contrib.auth.forms import UserCreationForm


class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = Post
        fields = ('title', 'body', 'image','type')
