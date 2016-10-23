from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.urls import reverse
from rest_framework import status

from .views import UserViewSet

class UserViewSetTests(APITestCase):
    def setUp(self):
        User.objects.create_superuser('superuser', 'test@test.com', 'test1234')

    def test_get_user(self):
        """
        Ensure we can create a new account object.
        """
        factory = APIRequestFactory()
        user = User.objects.get(username='superuser')
        view = UserViewSet.as_view({'get':'list'})

        # Make an authenticated request to the view...
        request = factory.get('/users/')
        force_authenticate(request, user=user)
        response = view(request)	 	
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertIn('"username":"superuser"', response.content)

    def test_create_valid_user(self):
	response = self.create_user('testUser')
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_user(self):
	response = self.create_user('I am an Invalid username')
	self.assertEqual(response.status_code, 400)

    def test_create_existing_user(self):
        User.objects.create_user(username='ExistingUser')
        response = self.create_user('ExistingUser')
        self.assertEqual(response.status_code, 400)
    
    def create_user(self, username):
	factory = APIRequestFactory()
        user = User.objects.get(username='superuser')
        view = UserViewSet.as_view({'post':'create'})
	request = factory.post('/users/', {"username":username}, format='json')
	force_authenticate(request, user=user)
        return view(request)                
