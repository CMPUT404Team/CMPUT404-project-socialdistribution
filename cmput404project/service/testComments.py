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

    def test_bad_author(self):
        #checks for no author comments
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        #no author
        pubDate = datetime.now()
        post = Post()
        comment = 'Nice doggo'
        try:
            comm = Comment().create_comment(comment, "abc", post)
        except ValueError:
            print(ValueError)

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

    #test get comments of a post
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

    # TODO test get comments of a non existant post
    def test_get_comment_no_post(self):
        pass

    #test create a comment through POST
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

    # TODO test update a comment through POST
    def test_post_update_comment(self):
        pass
