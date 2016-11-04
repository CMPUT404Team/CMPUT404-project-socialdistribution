from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid
from Author import Author
import datetime

@python_2_unicode_compatible
class Post(models.Model):
    VISIBILITY_OPTIONS = (('PU','PUBLIC'), ('PR','PRIVATE'),
    ('FR','FRIENDS'), ('FO','FOAF'), ('SO','SERVERONLY'))
    CONTENT_TYPE = (('text/plain','text/plain'),('text/markdown','text/markdown'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    published = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_OPTIONS, default= 'PUBLIC')
    title = models.CharField(max_length=75, blank=True)
    source = models.CharField(max_length=100, editable=False, blank=True)
    origin = models.CharField(max_length=100, editable=False, blank=True)
    description = models.CharField(max_length=200, blank=True)
    contentType = models.CharField(max_length=100, editable=False, default='text/plain')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.CharField(max_length=200, blank=True) #This would best be implemented by creating a categories model
    next = models.CharField(max_length=100, editable=False, blank=True)
    comments = []
    attached_photo = False
    count = models.IntegerField(default=0)
    size = models.IntegerField(default=50)

    @classmethod
    def create(cls, author,title,origin,description,categories,visibility):
        post = cls(author=author, title=title, origin=origin, description=description, categories=categories,
        visibility=visibility)
        post.origin = author.host
        post.source = author.host
        post.parse_description()
        post.comments = list(post.comment_set.all())
        post.next = "http://service/posts/" + str(post.id) +"/comments"
        return post

    def update_comment_count(self):
        count = len(self.comments)

    def __str__(self):
        return self.title

    def parse_description(self):
        if(self.markdown_description()):
            content_type = 'text/markdown'
        else:
            content_type = 'text/plain'
        if(self.posted_picture()):
            attached_photo = True
        else:
            attached_photo = False

    def markdown_description(self):
        return False

    def posted_picture(self):
        return False
