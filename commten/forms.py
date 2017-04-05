from commten.models import Tickets, User, Comment
from django import forms
from pagedown.widgets import PagedownWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=PagedownWidget(show_preview=False))

    class Meta:
        model = Tickets
        fields = ('title', 'status', 'type', 'body', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']