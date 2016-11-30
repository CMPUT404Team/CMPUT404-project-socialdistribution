from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
from models.Author import Author

class LoginForm(forms.Form):
    displayName = forms.CharField()
    password = forms.CharField(widget=PasswordInput)
