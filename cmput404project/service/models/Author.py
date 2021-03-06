from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse
import uuid

class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=100)
    displayName = models.CharField(max_length=30)
    user = models.OneToOneField(User, null=True)
    # Specifying symmetrical to false allows an Author to be friends with
    # another author who is not friends with them.
    friends = models.ManyToManyField("self", symmetrical=False, blank=True)

    @classmethod
    def create(cls, user, displayName, host):
        return cls(id=uuid.uuid4(), user=user, displayName=displayName, host=host)

    def add_friend(self, author):
        self.friends.add(author)

    def remove_friend(self, friend):
        self.friends.remove(friend)
    # Checks if one author is following another
    def is_following(self, uuid):
	return len(self.friends.filter(id=uuid))==1

    # Checks to see if both authors are friends with each other
    def is_friend(self,friend):
	return self.is_following(friend.id) and friend.is_following(self.id)

    # Get all friends of an author
    def get_friends(self):
	friends_list = []
	for friend in self.friends.all():
	    friends_list.append(friend.id)
	return friends_list

    def __str__(self):
        return self.displayName

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.id})
