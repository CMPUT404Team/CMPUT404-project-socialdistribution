from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate
from unittest import skip
from django.urls import reverse
from rest_framework import status
from models.Author import Author
import json

class UserViewSetTests(APITestCase):
    def setUp(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')       
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)
	self.author = Author.create(host='local', displayName='testMonkey', user=superuser)
	self.author.save()
	self.friend = Author.create(host='local', displayName='testMonkey2', user=superuser)
	self.friend.save()
	self.author.add_friend(self.friend)
	self.friend.add_friend(self.author)
        self.detail_url = reverse('friend-detail', kwargs={'uuid1': self.author.id, 'uuid2': self.friend.id})

    @skip ("Doesn't pass yet") 
    def test_get_friend_status(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(self.author.id), response.content)
	self.assertIn(str(self.friend.id), response.content)
	self.assertIn('true', response.content)
