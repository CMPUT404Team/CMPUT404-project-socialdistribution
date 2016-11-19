from rest_framework.test import APITestCase, APIClient, force_authenticate
from models.Post import Post
from models.Author import Author
from django.contrib.auth.models import User
import uuid
from django.core import serializers
import json
from unittest import skip

class PostPermissionsTests(APITestCase):

    def setUp(self):
        # an authorized client
        # an unauthorized client
        pass

    def test_private_auth_own(self):
        # see your own private posts
        # author 1, post 1 with private
        pass

    def test_private_auth_others(self):
        # unable to see others' private post
        # author 1, author 2, author 3 on different server, post 1 with PRIVATE and to author 2
        # check author 1+3 feed is empty
        pass

    def test_private_no_auth(self):
        # request not allowed
        pass

    def test_friends_auth_local(self):
        # can see posts of friends
        # author 1-2, 1 and 2 are friends local, 2 needs post with FRIENDS
        # 1 can see it
        pass

    def test_friends_auth_remote(self):
        # can see posts of friends
        # author 1-2, 1 and 2 are friends, 1 is local, 2 is remote, 2 needs post with FRIENDS
        # 1 can see it
        pass

    def test_friends_no_auth(self):
        # request not allowed
        pass

    def test_FOAF_auth_local(self):
        # author 1-3, 1 and 2 are friends, 2 and 3 are friends
        # 3 needs a post with FOAF
        # 1 can see it
        pass

    def test_FOAF_auth_remote(self):
        # author 1-3, 1 and 2 are friends, 2 and 3 are friends
        # 3 needs a post with FOAF
        # 1 can see it
        pass

    def test_FOAF_no_auth(self):
        # request not allowed
        pass

    def test_public_auth(self):
        # author 1-2-3, 2 has PUBLIC post, 1&3 can see it
        pass

    def test_public_no_auth(self):
        # request not allowed
        pass

    def test_serveronly_auth(self):
        # author 1-2 same server, author 3 on different server, 2 has post with SERVERONLY
        # author 1 can see, author 3 can't
        pass

    def test_serveronly_no_auth(self):
        # request not allowed
        pass

    def test_privateauthor_auth(self):
        # author 1-3, 2 has post visible to 1
        # 1 can see, 3 cannot see
        pass

    def test_privateauthor_no_auth(self):
        # request not allowed
        pass
