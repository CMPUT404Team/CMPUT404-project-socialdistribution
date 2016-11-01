from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
import uuid

class Author(models.Model):   
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=30)
    displayName = models.CharField(max_length=30)
    
    # Specifying symmetrical to false allows an Author to be friends with
    # another author who is not friends with them.
    friends = models.ManyToManyField("self", symmetrical=False, blank=True)
    
    class Meta:
        ordering = ('id',)

    def create_author(self, id, name):
        author = Author(id, name)
        
    def add_friend(self, author):
        self.friends.add(author)

    def __str__(self):
        return self.displayName
