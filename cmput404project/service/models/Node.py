from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse
import uuid

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=30)
    displayName = models.CharField(max_length=30)
    port = models.IntegerField(default=80)
    user = models.ForeignKey(User, null=True)
    
    @classmethod
    def create(cls, displayName, host, port, user):
        return cls(id=uuid.uuid4(),  displayName=displayName, host=host, port=port, user=user)

    def __str__(self):
        return self.displayName
