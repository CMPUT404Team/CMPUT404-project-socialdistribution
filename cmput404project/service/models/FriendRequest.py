from django.db import models
from Author import Author

class FriendRequest(models.Model):
    displayName = models.CharField(max_length=30)
    requesting_author_id = models.UUIDField(primary_key=True)
    author = models.ForeignKey(Author) 

    def __str__(self):
        return self.displayName
