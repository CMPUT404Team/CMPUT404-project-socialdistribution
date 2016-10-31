from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Post(models.Model):
    author = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    status = models.CharField(max_length=200)
    comments=[]#Comment class

    def __str__(self):
        return "Post"
    def createPost(self):
        author.getPosts().append(self)
    def changeStatus(self):
        return
    def deletePost(self):
        author.getPosts().remove(self)

    def addComment(self,comment):
        comments.append(com=Comment(comment))
