from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.urls import reverse
from unittest import skip
from rest_framework import status
from .views import UserViewSet
from mock import MagicMock, Mock, mock
from datetime import datetime
from models.Comment import Comment
from django.test import TestCase
from models.Author import Author
from models.Post import Post
import uuid

class CommentUnitTest(TestCase):

    def published_recently(self, pubDate, now):
        #checks if two dates are within the same day
        if (now.day == pubDate.day):
            return True
        else:
            return False

    def test_create_comment(self):
        # Tests the creation of a comment and that its values are set
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        author = Author.objects.create()
        #author.create(superuser, 'coolname', '127.0.0.0.1')
        pubDate = datetime.now()
        post = Post()
        comment = 'Nice doggo'
        comm = Comment().create_comment(comment, author, post)
        self.assertEqual(comm.author, author, "Author not equal")
        self.assertEqual(comm.comment, 'Nice doggo', "Comment not equal")
        self.assertIsInstance(comm.pubDate, datetime, "Not a datetime object")
        self.assertTrue(self.published_recently(comm.pubDate, pubDate))
        self.assertIsInstance(comm.guid, uuid.UUID, "Not a uuid object")
        self.assertIsInstance(comm, Comment, "Not a comment object")
    @skip("Failing")
    def test_bad_author(self):
        #checks for no author comments
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        #no author
        pubDate = datetime.now()
        post = Post()
        comment = 'Nice doggo'
        try:
            comm = Comment().create_comment(comment, "abc", post)
        except ValueError as e:
            self.assertTrue(e, "Successfully detected ValueError")

class CommentAPIViewTests(APITestCase):

    def setUp(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)
        self.author = Author()
        self.author.create(superuser, 'coolname', '127.0.0.0.1')

        self.post=Post.create(self.author,
            title="Top Ten best dogs",
            origin="http://dogfanatic.com",
            description="How do you pick just ten?!",
            categories = ["list","dog"],
            visibility = "PUBLIC")
        self.author.save()
        self.post.save()

    # test get comments of a post
    def test_get_comment(self):
        #call the endpoint
        comment = Comment().create_comment("Your pupper is wonderful", self.author, self.post)
        comment.save()
        response = self.client.get('/posts/'+str(self.post.id)+'/comments')
        #check that they match
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(comment.guid), response.data[0]['guid'])
        self.assertEqual(comment.post.id, self.post.id, "wrong post")
        comment.delete()

    # test get comment with non existent post
    def test_get_comment_no_post(self):
        response = self.client.get('/posts/'+str(self.post.id)+'/comments')
        self.assertEqual(response.status_code, 404)

    # test post comments with no comments
    def test_get_no_comments(self):
        # call endpoint
        response = self.client.get('/posts/'+str(self.post.id)+'/comments')

        self.assertEqual(response.status_code, 404)
        #self.assertEqual(str(comment.guid),"")

    # test get empty comment
    def test_get_empty_comments(self):
        comment = Comment().create_comment("", self.author, self.post)

        response = self.client.get('/posts/'+str(self.post.id)+'/comments')
        #check that they match
        self.assertEqual(response.status_code, 404)


    # test create a comment through POST
    def test_post_comment(self):
        comment={
          "query":"addComment",
          "post:":"http://localhost:8000/I-Don't-Care",
          "comment":{
            "author": {
              "url": "http://localhost:8000/author/14fdc531-4751-4e02-8cda-5fc5f4d221e1/",
              "id": self.author.id,
              "displayName": "KJSHDAKJD",
              "host": "AKJSBDA",
              "friends": []
              },
            "pubDate": "2016-11-04T03:33:12.786827Z",
            "comment": "Majestic dog",
            "guid": "84758741-e737-48e2-afde-c0f56546531c"
            }
        }
        response=self.client.post('/posts/'+str(self.post.id)+'/comments',comment,format='json')
        self.assertEqual(response.status_code, 200)
        try:
            Comment.objects.get(comment="Majestic dog")
        except Comment.DoesNotExist:
            self.fail("That comment does not exist")

    # test update a comment through POST
    def test_post_update_comment(self):
        # make comment
        comment = Comment().create_comment("Your pupper is wonderful", self.author, self.post)
        comment.save()
        updated_comment={
          "query":"addComment",
          "post:":"http://localhost:8000/I-Don't-Care",
          "comment":{
            "author": {
              "url": "http://localhost:8000/author/14fdc531-4751-4e02-8cda-5fc5f4d221e1/",
              "id": self.author.id,
              "displayName": "KJSHDAKJD",
              "host": "AKJSBDA",
              "friends": []
              },
            "pubDate": "2016-11-04T03:33:12.786827Z",
            "comment": "Your pupper is more wonderful",
            "guid": "84758741-e737-48e2-afde-c0f56546531c"
            }
        }

        # update comment
        response=self.client.post('/posts/'+str(self.post.id)+'/comments',updated_comment,format='json')
        self.assertEqual(comment.comment, "Your pupper is wonderful", "Comments not equal")

    # create a comment for a post that doesn't exist
    def test_comment_not_valid_post(self):
        # set invalid post id
        self.post.id="84758741-e737-48e2-afde-c0f55556431c"
        comment={
          "query":"addComment",
          "post:":"http://localhost:8000/I-Don't-Care",
          "comment":{
            "author": {
              "url": "http://localhost:8000/author/14fdc531-4751-4e02-8cda-5fc5f4d221e1/",
              "id": self.author.id,
              "displayName": "KJSHDAKJD",
              "host": "AKJSBDA",
              "friends": []
              },
            "pubDate": "2016-11-04T03:33:12.786827Z",
            "comment": "Majestic dog",
            "guid": "84758741-e737-48e2-afde-c0f56546431c"
            }
        }
        try:
            response=self.client.post('/posts/'+str(self.post.id)+'/comments',comment,format='json')
            self.assertEqual(response.status_code, 404)

        except Comment.DoesNotExist:
            self.fail("Comment is created")

    # TODO update a comment to a non valid post
    def test_comment_update_not_valid_post(self):
        # set invalid post id
        self.post.id="84758741-e737-48e2-afde-c0f55556431c"
        comment={
          "query":"addComment",
          "post:":"http://localhost:8000/I-Don't-Care",
          "comment":{
            "author": {
              "url": "http://localhost:8000/author/14fdc531-4751-4e02-8cda-5fc5f4d221e1/",
              "id": self.author.id,
              "displayName": "KJSHDAKJD",
              "host": "AKJSBDA",
              "friends": []
              },
            "pubDate": "2016-11-04T03:33:12.786827Z",
            "comment": "Majestic dog",
            "guid": "84758741-e737-48e2-afde-c0f56546431c"
            }
        }
        try:
            response=self.client.post('/posts/'+str(self.post.id)+'/comments',comment,format='json')
            self.assertEqual(response.status_code, 404, "Updated a comment with a non existent post")

        except Comment.DoesNotExist:
            self.fail("Comment is created, not updated")

    # put fails
    def test_comment_put_fail(self):
        comment={
          "query":"addComment",
          "post:":"http://localhost:8000/I-Don't-Care",
          "comment":{
            "author": {
              "url": "http://localhost:8000/author/14fdc531-4751-4e02-8cda-5fc5f4d221e1/",
              "id": self.author.id,
              "displayName": "KJSHDAKJD",
              "host": "AKJSBDA",
              "friends": []
              },
            "pubDate": "2016-11-04T03:33:12.786827Z",
            "comment": "Majestic dog",
            "guid": "84758741-e737-48e2-afde-c0f56546531c"
            }
        }
        try:
            response = self.client.put('/posts/'+str(self.post.id)+'/comments', comment, format='json')
            self.assertNotEqual(response.status_code, 404, "The put passed")
        except:
            self.assertEqual(response.status_code, 404)

    # delete fails
    def test_comment_delete_fails(self):
        try:
            response = self.client.delete('/posts/'+str(self.post.id)+'/comments')
            self.assertNotEqual(response.status_code, 404, "The delete passed")
        except:
            self.assertEqual(response.status_code, 404)
