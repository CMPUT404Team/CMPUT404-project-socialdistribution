from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.urls import reverse
from rest_framework import status

from .views import UserViewSet

class UserViewSetTests(APITestCase):
    def setUp(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)

    def test_get_valid_user(self):
        response = self.get_user(1)
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertIn('"username":"superuser"', response.content)

    def test_get_invalid_user(self):
        response = self.get_user(999)
        self.assertEqual(response.status_code, 404)

    def test_create_valid_user(self):
	response = self.create_user('testUser')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(User.objects.filter(username='testUser')), 1)

    def test_create_invalid_user(self):
	response = self.create_user('I am an Invalid username')
	self.assertEqual(response.status_code, 400)

    def test_create_existing_user(self):
        User.objects.create_user(username='ExistingUser')
        response = self.create_user('ExistingUser')
        self.assertEqual(response.status_code, 400)

    def get_user(self, user_id):
        """
        Ensure we can create a new account object.
        """
        return self.client.get('/users/'+str(user_id)+'/')

    def create_user(self, username):
        return self.client.post('/users/', {"username":username}, format='json')


class CommentTests(APITestCase):

    def setUp(self):
        #make author, post
        author = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        post = (post)
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)

    def test_get_comment(self):
        response = self.get_user(1)
        comment = Comment.create_comment("hello I am a comment", author)
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertIn('JSON GOES HERE', response.content)

    def test_post_comment(self):
        response = self.get_user(1)
        comment = Comment.create_comment("hello", author)
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertIn('JSON GOES HERE', response.content)
