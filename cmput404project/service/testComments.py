from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.urls import reverse
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

class CommentAPIViewTests(APITestCase):

    def setUp(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)
        self.author = Author()
        self.author.create(superuser, 'coolname', '127.0.0.0.1')
        self.post = Post()
        self.post.create(self.author,
            title="Top Ten best dogs",
            origin="http://dogfanatic.com",
            description="How do you pick just ten?!",
            categories = ["list","dog"],
            visibility = "PUBLIC")
        self.comment = Comment().create_comment("Your pupper is wonderful", self.author, self.post)
        self.author.save()
        self.post.save()
        self.comment.save()

    def test_get_comment(self):
        #call the endpoint
        response = self.client.get('/posts/'+str(self.post.id)+'/comments')
        #check that they match
        self.assertEqual(response.status_code, 200)
        print (response.content)
        self.assertIn(str(self.comment.guid), response.content)

    def test_post_comment(self):
        #check post comment from post object
        comment="this is a comment"
        self.post.addComment(comment)
        #assume there is only one comment??
        self.assertEqual(comment,self.post.get_comments())
