from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
from models.Author import Author

class AuthorExistsForm(forms.Form):
    displayName = forms.CharField()
