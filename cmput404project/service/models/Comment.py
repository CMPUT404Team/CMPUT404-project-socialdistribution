from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Comment(models.Model):
    author = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    comment=""
    def __init__(self,comm):
        comment=comm
    
