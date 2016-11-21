from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse
from Author import Author
from Node import Node
import uuid

class NodeManager(models.Model):
    @classmethod
    def create(cls):
        return cls()#(id=uuid.uuid4())

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(NodeManager, self).save(*args, **kwargs)

    def get_nodes(self):
        nodes = Node.objects.all()
        return nodes