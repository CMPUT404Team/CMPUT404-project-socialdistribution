from rest_framework.test import APITestCase, APIClient, force_authenticate
from models.Post import Post
from mock import MagicMock

class PostViewSetTests(APITestCase):
    def set_up(self):
        self.client = APIClient();

    def set_up_superuser(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        self.client.force_authenticate(user=superuser)

    def set_up_author(self):
        #base this off of how Author model is created
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

    def create_update_post(self, post_id, put_body):
        #PUT http://service/posts/postid to update/create post
        return self.client.put('/posts/'+str(post_id)+'/', put_body, format='json')

    def test_create_post_with_put(self):
        # Create a post using a put method
        post_id = 111
        put_body = {"postid":post_id, "title":"Sample Title"}
        response = self.create_update_post(post_id, put_body)
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        # Update an existing post
        post_id = 111
        post_body = {"postid":post_id, "title":"Sample Title"}
        response = self.create_post(post_body)
        put_body = {"title":"Updated Title"}
        response = self.create_update_post(post_id, put_body)
        self.assertEqual(response.status_code, 200)

    def test_update_nonexistent_post(self):
        # Try to update a post that hasn't been created
        # Maybe it should have the same result as test_create_post_with_put?
        post_id = 54321
        put_body = {"title":"Sample Title"}
        response = self.create_update_post(post_id, put_body)
        self.assertEqual(response.status_code, 404)

    def test_create_invalid_post(self):
        post_id = "not-a-number"
        put_body = {"title":"Sample Title"}
        response = self.create_update_post(post_id, put_body)
        self.assertEqual(response.status_code, 400)

    def test_create_existing_post(self):
        #TODO: create a post that already exists with a put
        # Seems like it is the same as test_update_post
        pass

    def create_post(self, post_body):
        #a POST should insert the post http://service/posts/postid
        return self.client.post('/posts/', post_body, format='json')

    def test_create_post_with_post(self):
        # Create a post using a post method
        request_body = {"postid":111}
        response = self.create_post(request_body)
        self.assertEqual(response.status_code, 200)

    def test_update_post_with_post(self):
        # Update an existing post
        request_body = {"postid":111, "title":"Sample Title"}
        response = self.create_post(request_body)
        request_body = {"title":"Updated Title"}
        response = self.create_post(request_body)
        self.assertEqual(response.status_code, 200)

    def test_creating_public_post(self):
        #TODO: create a public post and successfully query it
        pass

    def test_create_friend_post(self):
        #TODO: create a post that can only be seen by users friends
        pass

    def test_insert_invalid_post(self):
        #TODO: insert an invalidly formatted post
        pass
