from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from Post import Post

@python_2_unicode_compatible
class Category(models.Model):
    category = models.CharField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.category
