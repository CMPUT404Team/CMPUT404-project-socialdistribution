from django import forms
from django.contrib.auth.models import User
from models.Author import Author
from models.Post import Post

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
    description = forms.CharField(widget=forms.TextInput())
    content = forms.CharField(widget=forms.TextInput())
    visibility = forms.ChoiceField(widget=forms.Select, choices=VISIBILITY_OPTIONS)
    contentType = forms.ChoiceField(widget=forms.RadioSelect, choices=CONTENT_TYPE)
    categories = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CATEGORIES,
    )

    def create_post(self, author):
        #create(cls, author,title,origin,description,categories,visibility):
        post = Post.create(author, self.cleaned_data['title'], author.host, self.cleaned_data['description'],
            self.cleaned_data['categories'], self.cleaned_data['visibility'])
        post.save()
