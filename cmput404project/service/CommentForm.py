from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
from models.Comment import Comment

CONTENT_TYPE = (('text/plain','text/plain'),('text/markdown','text/markdown'))

class CommentForm(forms.Form):
    comment = forms.CharField()
    contentType = forms.ChoiceField(widget=forms.RadioSelect, choices=CONTENT_TYPE)

    def create_comment(self, author, post):
        comment = Comment.create_comment(self.cleaned_data['comment'], author,
            post, self.cleaned_data['contentType'])
        print comment
        comment.save()
