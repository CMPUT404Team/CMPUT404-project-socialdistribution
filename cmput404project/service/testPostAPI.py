from rest_framework.test import APITestCase, APIClient, force_authenticate
from models.Post import Post
from models.Author import Author
from django.contrib.auth.models import User
import uuid
from django.core import serializers
import json
from unittest import skip

class PostAPITests(APITestCase):
    def setUp(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)
        self.author = Author.create(host='local', displayName='testMonkey', user=superuser)
        self.author.save()
        self.post = Post.create(self.author,
            title="A post title about a post about web dev",
            origin="http://whereitcamefrom.com/post/zzzzz",
            description="This post discusses stuff -- brief",
            categories = ["web","tutorial"],
            visibility = "PUBLIC")
        self.post.save()

    def get_posts_by_current_user(self):
        return self.client.get('/author/posts/')
        #http://service/author/posts (posts that are visible to the currently authenticated user)

    def get_public_posts(self):
        # http://service/posts (all posts marked as public on the server)
        return self.client.get('/posts/')

    def get_posts_by_author_id(self, author_id):
        # http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
        return self.client.get('/author/'+str(author_id)+'/posts/')

    def get_posts_by_page(self, page_number):
        # GET http://service/author/posts?page=4
        return self.client.get('/author/posts?page='+str(page_number)+'/')

    def get_posts_by_page_and_size(self, page_number, size):
        # GET http://service/author/posts?page=4&size=50
        return self.client.get('/author/posts?page='+str(page_number)+'&size='+str(size)+'/')

    def get_single_post_by_id(self, post_id):
        # http://service/posts/{POST_ID} access to a single post with id = {POST_ID}
        return self.client.get('/posts/'+str(post_id)+'/')

    def create_post(self, post_body):
        #a POST should insert the post http://service/posts/postid
        return self.client.post('/posts/', data=post_body, format='json')

    def delete_post(self, post_id):
        #A delete should delete posts with a specific ID
        return self.client.delete('/posts/'+str(post_id)+'/')

    def create_update_post_with_put(self, post_id, put_body):
        #PUT http://service/posts/postid to update/create post
        return self.client.put('/posts/'+str(post_id)+'/', put_body, format='json')

    def create_update_post_with_post(self, post_id, post_body):
        return self.client.post('/posts/'+str(post_id)+'/', post_body, format='json')


    def test_get_posts_by_current_author(self):
        response = self.get_posts_by_current_user()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(self.post.id), response.data[0]['id'])
        self.assertEqual(str(self.post.author.id), response.data[0]['author']['id'])

    def test_no_posts_by_current_author(self):
        post_id = self.post.id
        # create posts when needed instead
        #self.delete_post(post_id)
        response = self.get_posts_by_current_user()
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(len(response.data), 0)

    def test_get_posts_by_current_admin(self):
        #TODO: Retrieves all the posts made by the currently logged in admin
        #how is it different from test_get_posts_by_current_author?
        pass

    def test_get_public_posts(self):
        # Retrieve all public posts on the server
        response = self.get_public_posts()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['visibility'], "PUBLIC")

    def test_get_posts_by_author_id(self):
        # Return all the posts made by an author with a specific ID
        response = self.get_posts_by_author_id(self.author.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(self.post.id), response.data[0]['id'])
        self.assertEqual(str(self.post.author.id), response.data[0]['author']['id'])

    def test_get_posts_with_invalid_author_id(self):
        # Get posts with an invalid author id, or author ID that doesn't exist
        not_author = uuid.uuid4()
        response = self.get_posts_by_author_id(not_author)
        self.assertEqual(response.status_code, 404)

    def test_get_post_by_id(self):
        response = self.get_single_post_by_id(self.post.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(str(self.post.id), response.data['id'])
        self.assertEqual(str(self.post.author.id), response.data['author']['id'])

    def test_get_posts_with_invalid_post_id(self):
        #TODO: tests behaviour for when you get posts with incorrectly
        #formatted ID, or ID that doesn't exist
        pass

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

    def test_get_posts_by_page_and_size(self):
        #TODO: retrieve a page of posts with specific size of page
        pass

    def test_get_posts_by_page_and_exceeded_size(self):
        #TODO: retrieve a page where there are more posts than the specified size
        pass

    def test_get_posts_by_page_and_partial_size(self):
        #TODO: retrive a page where the size is smaller than the one specified
        pass

    def create_update_post_with_put(self, post_id, put_body):
        #PUT http://service/posts/postid to update/create post
        return self.client.put('/posts/'+str(post_id)+'/', put_body, format='json')

    def create_post_to_id(self, post_id, put_body):
        return self.client.post('/posts/'+str(post_id)+'/', put_body, format='json')

    def test_create_post_with_put(self):
        self.post.id = uuid.uuid4()
        request_body = self.get_post_data(self.post, self.author)
        response = self.create_update_post_with_put(self.post.id, request_body)
        self.assertEqual(response.status_code, 200)

    def test_update_post_with_put(self):
        # Create a post using a put method
        self.post.title = "The new title"
        put_body = self.get_post_data(self.post, self.author)
        response = self.create_update_post_with_put(self.post.id, put_body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "The new title")

    def test_create_invalid_post(self):
        self.post.id = "not-a-number"
        put_body = self.get_post_data(self.post, self.author)
        response = self.create_update_post_with_post(self.post.id, put_body)
        self.assertEqual(response.status_code, 400)

    def test_delete_post(self):
        post_id = self.post.id
        response = self.delete_post(post_id)
        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_post(self):
        post_id = uuid.uuid4()
        response = self.delete_post(post_id)
        self.assertEqual(response.status_code, 404)

    def test_author_deletes_own_post(self):
        #TODO: check permissions for an author deleting their own post
        pass

    def test_admin_deletes_post(self):
        #TODO: an admin can delete any post, regardless if they authored it
        pass

    def test_create_post_with_post(self):
        # Create a post using a post method
        self.post.id = uuid.uuid4()
        request_body = self.get_post_data(self.post, self.author)
        response = self.create_post(request_body)
        self.assertEqual(response.status_code, 201)

    def test_create_post_to_id(self):
        # Create a post using a post method
        self.post.id = uuid.uuid4()
        request_body = self.get_post_data(self.post, self.author)
        response = self.create_post_to_id(self.post.id, request_body)
        self.assertEqual(response.status_code, 200)
        pass

    def test_update_post_with_post(self):
        # Update an existing post
        request_body = self.get_post_data(self.post, self.author)
        response = self.create_update_post_with_post(self.post.id, request_body)
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

    def get_post_data(self, post, author):
        return {
            "title": post.title,
            "source": post.source,
            "origin": post.origin,
            "description": post.description,
            "contentType": post.contentType,
            "content": post.content,
            "author":{
                "id": str(author.id),
                "host": author.host,
                "displayName": author.displayName,
            },
            "categories": post.categories,
            "count": str(post.count),
            "size": str(post.size),
            "next": post.next,
            "published":str(post.published),
            "id":str(post.id),
            "visibility":post.visibility
        }
