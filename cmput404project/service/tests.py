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

    def test_create_user(self):
        pass
