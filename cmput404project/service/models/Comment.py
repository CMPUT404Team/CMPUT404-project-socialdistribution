from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid
from datetime import datetime

'''
Assumptions based on requirements
- Comments cannot be images
- Comments are plain text only
- Can only create comments, no delete or edit
- If you can see the post, you can see all comments
'''
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
        createdComment.pubDate = datetime.now()
        return createdComment
        
    def __str__(self):
        return self.comment
