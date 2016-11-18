from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate
from unittest import skip
from django.urls import reverse
from rest_framework import status
from models.Author import Author
from AuthorForm import AuthorForm
import json

class AuthorAPITests(APITestCase):
    def setUp(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')       
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)
	self.author = Author.create(host='local', displayName='testMonkey', user=superuser)
	self.author.save()
        self.detail_url = reverse('author-detail', kwargs={'pk': self.author.id})
    
    def test_get_Author(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.author.displayName, response.content)

    def test_get_friends(self):
	friend = Author(host='testHost', displayName='testName')
	friend.save()
	self.author.add_friend(friend)
	response = self.client.get(self.detail_url)
	json_friend = response.data.get('friends')[0]
	self.assertIn('testHost',json_friend['host'])
	self.assertIn('testName',json_friend['displayName'])	
        
class AddAuthorApiTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.add_url = reverse('author-add')

    def test_add_new_author(self):
        form = AuthorForm({'displayName':'Yolo Swag', 'password':'4ForLife'})
        if (form.is_valid()):
            response = self.client.post(self.add_url, form.cleaned_data)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, reverse('awaiting-approval'))
        else:
            self.fail("You passed invalid data to the form")

    def test_add_new_author_with_existing_username(self):
        self.fail()
    def test_new_author_is_not_active(self):
        self.fail()

    def get_valid_author_form_data(self):
        self.fail()
