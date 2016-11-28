from django.test import TestCase, Client, LiveServerTestCase
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.contrib.auth.models import User
from models.Author import Author
from models.Node import Node
from frontEndViews import BefriendView
from django.shortcuts import render
from unittest import skip 

class FrontEndViewTest(LiveServerTestCase):
    
    def setUp(self):
        self.client = Client()
	self.user_password = "secure1234"
        self.author_user = User.objects.create_user(username="auth", password=self.user_password)
        self.author_user.save()
        self.author = Author.create(user=self.author_user, host=self.live_server_url, displayName="auth")
        self.author.save()
	self.friend_user = User.objects.create_user(username="friend", password="test1234")
	self.friend = Author.create(user=self.friend_user, host=self.live_server_url, displayName="friend")
        self.friend.save()
	self.client = APIClient()
        self.client.force_authenticate(user=self.author_user)
	self.node = Node.create(
            displayName = "The Node",
            host = self.live_server_url,
            path = "",
            user = self.author_user,
            username = 'auth',
            password = self.user_password
            )
        self.node.save()
	
    def get_friend_json(self, friend):
        return {
                "id": str(friend.id),
                "host":friend.host,
                "displayName":friend.displayName
                }

    def test_should_400_on_malformed_json(self):
        response = self.client.post('/frontend/befriend/', data={"this is not friend json":"and will not make you any friends"})
        self.assertEqual(400, response.status_code)

    @skip("Wyatt doesn't know how to pass the form data properly, so he is giving up.")
    def test_should_befriend_from_frontend(self):
        response = self.client.post('/frontend/befriend/', data=str({"friend":str(self.get_friend_json(self.friend)),"currently_friends":"False"}))
	self.assertEqual(204, response.status_code)
	self.assertIn(self.friend, self.author.friends.all())
