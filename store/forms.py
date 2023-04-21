from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductSearchForm(forms.Form):
    name = forms.CharField(label='Название продукта', max_length=255)
