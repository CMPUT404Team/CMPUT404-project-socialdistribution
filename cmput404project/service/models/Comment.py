from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from Post import Post

@python_2_unicode_compatible
class Comment(models.Model):
    pub_date = models.DateTimeField('date published')
    comment=models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    def __str__(self):
        return self.comment
