from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse
import uuid, base64, urllib2
import json

class Node(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    displayName = models.CharField(max_length=30)
    host = models.CharField(max_length=100)
    path = models.CharField(max_length=100, default='')
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
            password = base64.b64encode(password)
            )

    def __str__(self):
        return self.displayName

    def get_posts(self):
        baseUrl = 'http://' + self.host + self.path
        url = baseUrl + "/author/posts"
        r = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        r.add_header("Authorization", "Basic %s" % base64string)
        f = urllib2.urlopen(r).read()
        posts = json.loads(f)
        return posts

    def get_posts_by_author(self, author_id):
        baseUrl = 'http://' + self.host + self.path
        url = baseUrl + "/posts"
        try:
            r = urllib2.Request(url)
            base64string = base64.b64encode('%s:%s' % (self.username, self.password))
            r.add_header("Authorization", "Basic %s" % base64string)
            f = urllib2.urlopen(r).read()
            posts = json.loads(f)
        except ValueError:
            posts = {}
        return posts

    def get_public_posts(self):
        baseUrl = 'http://' + self.host + self.path
        url = baseUrl + "/posts"
        r = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        r.add_header("Authorization", "Basic %s" % base64string)
        f = urllib2.urlopen(r).read()
        posts = json.loads(f)
        return posts
