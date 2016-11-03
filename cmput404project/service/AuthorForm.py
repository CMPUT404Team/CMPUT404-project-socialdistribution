from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
from models.Author import Author

class AuthorForm(forms.Form):
    displayName = forms.CharField()
    password = forms.CharField(widget=PasswordInput)
    
    def create_author(self, host):
        user = User.objects.create_user(username=self.cleaned_data['displayName'], password=self.cleaned_data['password'])
        user.save()
        author = Author.create(user, self.cleaned_data['displayName'], host)
        author.save()
        return author.get_absolute_url()
