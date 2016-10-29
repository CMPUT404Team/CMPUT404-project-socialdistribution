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

    def get_posts_by_current_user(self):
        return self.client.get('/author/posts/')
        #http://service/author/posts (posts that are visible to the currently authenticated user)

    def test_get_posts_by_current_author(self):
        #TODO: Retrives all the posts made by the currently logged in author
        pass

    def test_get_posts_by_current_admin(self):
        #TODO: Retrieves all the posts made by the currently logged in admin
        pass

    def get_public_posts(self):
        # http://service/posts (all posts marked as public on the server)
        return self.client.get('/posts/')

    def test_get_public_posts(self):
        #TODO: Retrieve all public posts on the server
        pass

    def get_posts_by_author_id(self, author_id):
        # http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
        return self.client.get('/author/'+str(author_id)+'/')

    def test_get_posts_by_author_id(self):
        #TODO: returns all the posts made by an author with a specific ID
        pass

    def test_get_posts_with_invalid_author_id(self):
        #TODO: test getting posts with an invalid author id, or author ID that doesn't exist
        pass

    def get_single_post_by_id(self, post_id):
        # http://service/posts/{POST_ID} access to a single post with id = {POST_ID}
        return self.client.get('/posts/'+str(post_id)+'/')

    def test_get_post_by_id(self):
        #TODO: Retrieves the post by its unique ID
        pass

    def test_get_posts_with_invalid_post_id(self):
        #TODO: tests behaviour for when you get posts with incorrectly
        #      formatted ID, or ID that doesn't exist
        pass

    def get_posts_by_page(self, page_number):
        # GET http://service/author/posts?page=4
        return self.client.get('/author/posts?page='+str(page_number)+'/')

    def test_get_posts_by_page(self):
        #TODO: Returns all of posts on a specific page
        pass

    def test_get_full_page_of_posts(self):
        #TODO: test retrieving a full page of posts
        pass

    def test_get_partial_page_of_posts(self):
        #TODO: test retrieving a partial page of posts
        pass

    def test_page_does_not_exist(self):
        #TODO: Tests what is returned if requested page of posts does not exist
        pass

    def test_page_has_no_posts(self):
        #TODO: Tests getting page 1, when the user has made no posts
        #pretty sure this is redundant to above
        pass

    def get_posts_by_page_and_size(self, page_number, size):
        # GET http://service/author/posts?page=4&size=50
        return self.client.get('/author/posts?page='+str(page_number)+'&size='+str(size)+'/')

    def test_get_posts_by_page_and_size(self):
        #TODO: retrieve a page of posts with specific size of page
        pass

    def test_get_posts_by_page_and_exceeded_size(self):
        #TODO: retrieve a page where there are more posts than the specified size
        pass

    def test_get_posts_by_page_and_partial_size(self):
        #TODO: retrive a page where the size is smaller than the one specified
        pass

    def create_update_post(self, post_id):
        #PUT http://service/posts/postid to update/create post
        return self.client.put('/posts/'+str(post_id)+'/', {"postid":post_id}, format='json')

    def test_create_post_with_put(self):
        #TODO: Create a post using a put method
        pass

    def test_update_post(self):
        #TODO: Update an existing post
        pass

    def test_update_nonexistent_post(self):
        #TODO: try to update a post that hasn't been created
        pass

    def test_create_invalid_post(self):
        #TODO: create a post that has an invalid post_id
        # maybe unessecary?
        pass

    def test_create_existing_post(self):
        #TODO: create a post that already exists with a put
        pass

    def create_post(self, post_id):
        #a POST should insert the post http://service/posts/postid
        return self.client.post('/posts/'+str(post_id)+'/',{"postid":post_id}, format='json')

    def test_create_post_with_post(self):
        #TODO: Create a post using a post method
        post_id = 111
        response = self.create_post(111)
        self.assertEqual(response.status_code, 201)

    def test_update_post_with_post(self):
        #TODO: Update an existing post
        post_id = 111
        self.create_post(111)
        response = self.create_post(111)
        self.assertEqual(response.status_code, 200)

    def test_insert_into_existing(self):
        #TODO: try to post into an existing post
        pass

    def test_insert_invalid_post(self):
        #TODO: insert an invalidly formatted post
        pass
