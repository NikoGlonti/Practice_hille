from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class PostCreate(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'brief_description', 'full_description', 'posted']


class CommentCreate(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'posted_com']


class ContactUsForm(forms.Form):
    email = forms.EmailField(required=True)
    text = forms.CharField(max_length=400, help_text="Describe your problem")

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
