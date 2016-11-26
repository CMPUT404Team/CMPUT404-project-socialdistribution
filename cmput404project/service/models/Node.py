from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse
import uuid, urllib2
import json
import requests

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=30)
    host = models.CharField(max_length=100)
    path = models.CharField(max_length=100, default='', blank=True)
    user = models.ForeignKey(User, null=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    @classmethod
    def create(cls, displayName, host, path, user, username, password):
        return cls(
            id = uuid.uuid4(),
            displayName = displayName,
            host = host,
            path = path,
            user = user,
            username = username,
            password = password,
            )

    def __str__(self):
        return self.displayName
   
    def get_base_url(self):
        return 'http://' + self.host + self.path

    def make_authenticated_request(self, url):
        return requests.get(url, auth=(self.username,self.password))

    def get_json(self, url):
        r = self.make_authenticated_request(url)
        if (r.status_code == 200):
            return r.json()

    def get_posts(self):
        url = self.get_base_url() + "/author/posts"
        return self.get_json(url) 

    def get_posts_by_author(self, author_id):
        url = self.get_base_url() + "/author/" + str(author_id) + "/posts"
        return self.get_json(url)

    def get_public_posts(self):
        url = self.get_base_url() + "/posts"
        return self.get_json(url)
