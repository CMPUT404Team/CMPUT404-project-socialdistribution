from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid
from Author import Author
import datetime

class Post(models.Model):
    VISIBILITY_OPTIONS = (('PUBLIC','PUBLIC'), ('PRIVATE','PRIVATE'),
    ('FRIENDS','FRIENDS'), ('FOAF','FOAF'), ('SERVERONLY','SERVERONLY'))
    CONTENT_TYPE = (('text/plain','text/plain'),('text/markdown','text/markdown'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    published = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_OPTIONS, default= 'PUBLIC')
    title = models.CharField(max_length=75)
    source = models.CharField(max_length=100, editable=False)
    origin = models.CharField(max_length=100, editable=False)
    description = models.CharField(max_length=200, blank=True)
    content = models.CharField(max_length=200, blank=True)
    contentType = models.CharField(max_length=100, choices=CONTENT_TYPE, default='text/plain')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.CharField(max_length=200, blank=True) #This would best be implemented by creating a categories model
    comments = []

    @classmethod
    def create(cls, author,title,origin,description,categories,visibility, content, contentType):
        post = cls(author=author, title=title, origin=origin, description=description, categories=categories,
        visibility=visibility, content=content, contentType=contentType)
        post.origin = author.host
        post.source = author.host
        post.id = uuid.uuid4()
        post.origin = "http://" + author.host +"/posts/" + str(post.id)
        post.source = "http://" + author.host +"/posts/" + str(post.id)
        post.parse_description()
        return post

    def __str__(self):
        return self.title

    def parse_description(self):
        if(self.markdown_description()):
            content_type = 'text/markdown'
        else:
            content_type = 'text/plain'

    def markdown_description(self):
        return False

    def posted_picture(self):
        return False
