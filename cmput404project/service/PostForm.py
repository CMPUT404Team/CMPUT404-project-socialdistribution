from django import forms
from django.contrib.auth.models import User
from models.Author import Author

VISIBILITY_OPTIONS = (('PUBLIC','PUBLIC'), ('PRIVATE','PRIVATE'),
('FRIENDS','FRIENDS'), ('FOAF','FOAF'), ('SERVERONLY','SERVERONLY'))
CONTENT_TYPE = (('text/plain','text/plain'),('text/markdown','text/markdown'))
CATEGORIES = (
    ('tutorial','Tutorial'),
    ('dogs','Dogs'),
    ('corgi','Corgi'),
    ('puppy','puppy')
)

class PostForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.TextInput(), required=False)
    content = forms.CharField(widget=forms.TextInput(), required=False)
    visibility = forms.ChoiceField(widget=forms.Select, choices=VISIBILITY_OPTIONS)
    contentType = forms.ChoiceField(widget=forms.RadioSelect, choices=CONTENT_TYPE)
    categories = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CATEGORIES,
    )

    def create_post(self, host):
        print "creating post", host
