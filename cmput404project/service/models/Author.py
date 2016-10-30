from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
import uuid

class Author(models.Model):   
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=30)
    displayName = models.CharField(max_length=30) 
    friends = models.ManyToManyField("self", symmetrical=False)

    def add_friend(self, author):
        self.friends.add(author)
