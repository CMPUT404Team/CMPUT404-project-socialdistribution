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
        superuser2 = User.objects.create_superuser('superuser2', 'test2@test.com', 'test1234')
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)
    	self.friend1 = Author.create(host='local', displayName='testMonkey1', user=superuser)
    	self.friend1.save()
    	self.friend2 = Author.create(host='local', displayName='testMonkey2', user=superuser2)
    	self.friend2.save()

    def test_check_valid_friends(self):
	# Should not be friends at this point
	self.assertFalse(self.friend1.is_friend(self.friend2))
	self.friend1.add_friend(self.friend2)
	self.friend2.add_friend(self.friend1)
	# Friends have been added now
	self.assertTrue(self.friend1.is_friend(self.friend2))

    def test_check_invalid_friends(self):
	# Test against invalid ID
	self.assertFalse(self.friend1.is_following('0b141e54-c35a-4cc6-8864-bd584ec95a25'))

    def test_get_friend_list(self):
	# Test to get a list of author's friends
	# Before friend added to author
	self.assertEqual(len(self.friend1.get_friends()), 0)
	self.friend1.add_friend(self.friend2)
	# After friend is added to author
	self.assertEqual(len(self.friend1.get_friends()), 1)
