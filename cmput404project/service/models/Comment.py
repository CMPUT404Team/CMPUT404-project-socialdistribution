from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid

@python_2_unicode_compatible
class Comment(models.Model):
    author = models.CharField(max_length=200)
    pubDate = models.DateTimeField('date published')
    comment= models.CharField(max_length=200)
    guid = models.CharField(primary_key=True, max_length=200)

    @classmethod
    def create_comment(cls,comm, auth):
        createdComment = cls(comment = comm, author = auth)
        createdComment.guid = uuid.uuid4()
        return createdComment
