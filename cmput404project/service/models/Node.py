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
        return self.host + self.path

    def make_authenticated_request(self, url):
        return requests.get(url, auth=(self.username,self.password))

    def make_authenticated_post_request(self, url, data):
        return requests.post(url, auth=(self.username,self.password), json=data, allow_redirects=True)

    def get_friend_request_json(self, author_json, friend_json):
        return {
                "query":"friendrequest",
                "author": author_json,
                "friend": friend_json
                }

    def get_json(self, url):
        r = self.make_authenticated_request(url)
        if (r.status_code == 200):
            try:
                return r.json()
            except:
                return None

    def get_post(self, post_id):
        url = self.get_base_url() + "/posts/" + str(post_id)
        return self.get_json(url)

    def get_posts(self):
        url = self.get_base_url() + "/author/posts?page=1&size=1000"
        return self.get_json(url)

    def get_posts_by_author(self, author_id):
        url = self.get_base_url() + "/author/" + str(author_id) + "/posts"
        return self.get_json(url)

    def get_public_posts(self):
        url = self.get_base_url() + "/posts"
        return self.get_json(url)

    def befriend(self, author_json, friend_json):
        url = self.get_base_url() + "/friendrequest/"
        r = self.make_authenticated_post_request(url, self.get_friend_request_json(author_json, friend_json))
        return r.status_code

    def get_author(self, author_id):
        url = self.get_base_url() + "/author/" + str(author_id)
        r = self.make_authenticated_request(url)
	if (r.status_code == 200):
        	return r.json()

    def are_friends(self, id1, id2):
        url = self.get_base_url() + "/friends/" + str(id1) + "/" + str(id2)
        response = self.get_json(url)
        return (response != None and response['friends'] == True)

    def get_comments(self, post_id):
        url = self.get_base_url()+'/posts/' + str(post_id) + "/comments"
        response = self.get_json(url)
        return response
