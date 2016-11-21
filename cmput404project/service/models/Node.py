from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse
import uuid, base64, requests

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=30)
    host = models.CharField(max_length=100)
    port = models.IntegerField(default=80)
    user = models.ForeignKey(User, null=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    @classmethod
    def create(cls, displayName, host, port, user, username, password):
        return cls(
            id = uuid.uuid4(),
            displayName = displayName,
            host = host,
            port = port,
            user = user,
            username = username,
            password = password
            )

    def __str__(self):
        return self.displayName

    def get_posts(self):
        baseUrl = 'http://' + self.host + ':' + str(self.port)
        url = baseUrl + "/author/posts"
        r = requests.get(url, auth=(self.username, base64.b64decode(self.password)))
        posts = r.json()
        return posts

    def get_posts_by_author(self, author_id):
        baseUrl = 'http://' + self.host + ':' + str(self.port)
        url = baseUrl+ "/author/" + str(author_id) + "/posts"
        r = requests.get(url, auth=(self.username, base64.b64decode(self.password)))
        try:
            posts = r.json()
        except ValueError:
            posts = []
        return posts