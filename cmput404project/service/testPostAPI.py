from rest_framework.test import APITestCase, APIClient, force_authenticate
from models.Post import Post
from models.Author import Author
# from mock import MagicMock
from django.contrib.auth.models import User
import uuid
from django.core import serializers
import json

class PostViewSetTests(APITestCase):
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
        
    #def set_up_author(self):
        #base this off of how Author model is created
    #    self.author = Mock()
    #    self.client.force_authenticate(user=author)

    def get_posts_by_current_user(self):
        return self.client.get('/author/posts/')
        #http://service/author/posts (posts that are visible to the currently authenticated user)

    def get_public_posts(self):
        # http://service/posts (all posts marked as public on the server)
        return self.client.get('/posts/')

    def get_posts_by_author_id(self, author_id):
        # http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
        return self.client.get('/author/'+str(author_id)+'/')

    def get_single_post_by_id(self, post_id):
        # http://service/posts/{POST_ID} access to a single post with id = {POST_ID}
        return self.client.get('/posts/'+post_id+'/')

    def get_posts_by_page(self, page_number):
        # GET http://service/author/posts?page=4
        return self.client.get('/author/posts?page='+str(page_number)+'/')

    def get_posts_by_page_and_size(self, page_number, size):
        # GET http://service/author/posts?page=4&size=50
        return self.client.get('/author/posts?page='+str(page_number)+'&size='+str(size)+'/')

    def create_post(self, post_body):
        #a POST should insert the post http://service/posts/postid
        return self.client.post('/posts/', post_body, format='json')

    def delete_post(self, post_id):
        #A delete should delete posts with a specific ID
        return self.client.delete('/posts/'+str(post_id)+'/')

    def create_update_post(self, post_id, put_body):
        #PUT http://service/posts/postid to update/create post
        print '\n'
        return self.client.put('/posts/'+str(post_id)+'/', put_body, format='json')

    def test_get_posts_by_current_author(self):
        put_body = {"id":str(self.post.id), "author":str(self.author.id), "title":"Sample Title"}
        self.create_update_post(self.post.id, put_body)
        response = self.get_posts_by_current_user()
        self.assertEqual(response.status_code, 200)

    def test_no_posts_by_current_author(self):
        pass

    def test_get_posts_by_current_admin(self):
        #TODO: Retrieves all the posts made by the currently logged in admin
        pass

    def test_get_public_posts(self):
        #TODO: Retrieve all public posts on the server
        pass

    def test_get_posts_by_author_id(self):
        #TODO: returns all the posts made by an author with a specific ID
        pass

    def test_get_posts_with_invalid_author_id(self):
        #TODO: test getting posts with an invalid author id, or author ID that doesn't exist
        pass

    def test_get_post_by_id(self):
        #TODO: Retrieves the post by its unique ID
        pass

    def test_get_posts_with_invalid_post_id(self):
        #TODO: tests behaviour for when you get posts with incorrectly
        #      formatted ID, or ID that doesn't exist
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

    def test_create_post_with_put(self):
        # Create a post using a put method
        post_body = self.get_post_data(self.post, self.author)
        print json.dumps(post_body, sort_keys=True,indent=4, separators=(',', ': '))
        response = self.create_update_post(self.post.id, post_body)
        print str(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        # Update an existing post
        post_body = {"id":str(self.post.id), "title":"Sample Title"}
        response = self.create_post(post_body)
        put_body = {"title":"Updated Title"}
        response = self.create_update_post(self.post.id, put_body)
        self.assertEqual(response.status_code, 200)

    def test_update_nonexistent_post(self):
        # Try to update a post that hasn't been created
        # Maybe it should have the same result as test_create_post_with_put?
        post_id = uuid.uuid4()
        put_body = {"title":"Sample Title"}
        response = self.create_update_post(post_id, put_body)
        self.assertEqual(response.status_code, 404)

    def test_create_invalid_post(self):
        post_id = "not-a-number"
        put_body = {"title":"Sample Title"}
        try:
            response = self.create_update_post(post_id, put_body)
            self.assertEqual(response.status_code, 400)
        except ValueError:
            pass

    def test_delete_post(self):
        post_id = self.post.id
        response = self.delete_post(post_id)
        self.assertEqual(response.status_code, 200)

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
        request_body = {"id":str(self.post.id)}
        response = self.create_post(request_body)
        self.assertEqual(response.status_code, 200)

    def test_update_post_with_post(self):
        # Update an existing post
        request_body = {"id":str(self.post.id), "title":"Updated Title"}
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

    def get_post_data(self, post, author):
        return { 
            # title of a post
			"title": post.title,
			# where did you get this post from?
			"source": post.source,
			# where is it actually from
			"origin": post.origin,
			# a brief description of the post
			"description": post.description,
			# The content type of the post
			# assume either
			# text/x-markdown
			# text/plain
			# for HTML you will want to strip tags before displaying
			"contentType": post.contentType,
			"content": post.content,
			# the author has an ID where by authors can be disambiguated 
			"author":{
				# ID of the Author (UUID) http://en.wikipedia.org/wiki/Universally_unique_identifier
				"id": str(author.id),
				# the home host of the author
				"host": author.host,
				# the display name of the author
				"displayName": author.displayName,
			},
			# categories this post fits into (a list of strings
			"categories": post.categories,
			# comments about the post
			# return a maximum number of comments
			# total number of comments for this post
			"count": str(post.count),
			# page size
			"size": str(post.size),
			# the first page of comments
			"next": post.next,
			# You should return ~ 5 comments per post.
			# should be sorted newest(first) to oldest(last) 
			"comments":[
				{
					"author":{
					    # ID of the Author (UUID)
						"id":"de305d54-75b4-431b-adb2-eb6b9e546013",
						"host":"http://127.0.0.1:5454/",
						"displayName":"Greg Johnson",
						# url to the authors information
						"url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
						# HATEOS url for Github API
						"github": "http://github.com/gjohnson"
					},
					"comment":"Sick Olde English",
					"contentType":"text/x-markdown",
					# ISO 8601 TIMESTAMP
					"published":"2015-03-09T13:07:04+00:00",
					# ID of the Comment (UUID)
					"id":"de305d54-75b4-431b-adb2-eb6b9e546013"
				}
			],
			# ISO 8601 TIMESTAMP
			"published":str(post.published),
			# ID of the Post (UUID)
			"id":str(post.id),
			# visibility ["PUBLIC","FOAF","FRIENDS","PRIVATE","SERVERONLY"]
			"visibility":post.visibility
        }
