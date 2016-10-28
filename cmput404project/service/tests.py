from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.urls import reverse
from rest_framework import status
from models import Author

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

class PostViewSetTests(APITestCase):
    def set_up(self):
        self.client = APIClient();

    def set_up_superuser(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        self.client.force_authenticate(user=superuser)

    def set_up_author(self):
        #base this off of how Author model is created
        author = Author.objects.create_author('Username')
        self.client.force_authenticate(user=author)

    #Defining our GET endpoints that we need to test
    def get_posts_by_current_user(self):
        #http://service/author/posts (posts that are visible to the currently authenticated user)
        return self.client.get('/author/posts/')

    def get_public_posts(self):
        # http://service/posts (all posts marked as public on the server)
        return self.client.get('/posts/')

    def get_posts_by_author_id(self, author_id):
        # http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
        return self.client.get('/author/'+str(author_id)+'/')

    def get_single_post_by_id(self, post_id):
        # http://service/posts/{POST_ID} access to a single post with id = {POST_ID}
        return self.client.get('/posts/'+str(post_id)+'/')

    def get_posts_by_page(self, page_number):
        # GET http://service/author/posts?page=4
        return self.client.get('/author/posts?page='+str(page_number)+'/')

    def get_posts_by_page_and_size(self, page_number, size):
        # GET http://service/author/posts?page=4&size=50
        return self.client.get('/author/posts?page='+str(page_number)+'&size='+str(size)+'/')

    def create_update_post(self, post_id):
        #PUT http://service/posts/postid to update/create post
        return self.client.put('/posts/'+str(post_id)+'/', {"postid":post_id}, format='json')

    def create_post(self, post_id):
        #a POST should insert the post http://service/posts/postid
        return self.client.post('/posts/'+str(post_id)+'/'{"postid":post_id}, format='json')
