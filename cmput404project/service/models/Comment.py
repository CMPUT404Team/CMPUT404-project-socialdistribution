from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import uuid
from Post import Post
from Author import Author

'''
Assumptions based on requirements
- Comments cannot be images
- Comments are plain text only
- Can only create comments, no delete or edit
- If you can see the post, you can see all comments
'''
#@python_2_unicode_compatible
class Comment(models.Model):
    CONTENT_TYPE = (('text/plain','text/plain'),('text/markdown','text/markdown'))

    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    pubDate = models.DateTimeField(default=timezone.now, null=True)
    comment = models.CharField(max_length=200)
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contentType = models.CharField(max_length=100, choices=CONTENT_TYPE, default='text/plain')

    @classmethod
    def create_comment(cls,comm, auth, post, ct):
        if(comm!="" and (comm is not None)):
            createdComment = cls(comment = comm, author = auth, post = post, contentType = ct)
        else:
            createdComment=None
        return createdComment

    def __str__(self):
        return self.comment
