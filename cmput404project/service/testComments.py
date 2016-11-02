from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.urls import reverse
from rest_framework import status
from .views import UserViewSet
from mock import MagicMock, Mock
from datetime import datetime
from models.Comment import Comment
from django.test import TestCase
import uuid

class CommentUnitTest(TestCase):

    def published_recently(self, pubDate, now):
        if (now.day == pubDate.day):
            return True
        else:
            return False

    def test_create_comment(self):
        author = Mock(id = 'de305d54-75b4-431b-adb2-eb6b9e546013', host = 'http://127.0.0.1:5454/', displayName = 'Greg')
        #pubDate = datetime.now()
        comment = 'This is a comment'
        comm = Comment().create_comment(comment, author)
        comm.guid = uuid.UUID('de305d54-75b4-431b-adb2-eb6b9e546023')
        self.assertEqual(comm.author, author, "Author not equal")
        self.assertEqual(comm.comment, comment, "Comment not equal")
        self.assertEqual(comm.guid, uuid.UUID('de305d54-75b4-431b-adb2-eb6b9e546023'), "UUID not equal")
        #print type(comm.pubDate)
        #print comm.pubDate
        #self.assertIsInstance(comm.pubDate, datetime, "Not a datetime object")
        #self.assertTrue(self.published_recently(comm.pubDate, datetime.now()), "Date not recent enough")
        #self.assertIsInstance(comm.guid, uuid.uuid4(), "Not a uuid object")
        self.assertIsInstance(comm, Comment, "Not a comment object")

class CommentAPIViewTests(APITestCase):

    def setUp(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)
        self.author = Mock(id = 'de305d54-75b4-431b-adb2-eb6b9e546013', host = 'http://127.0.0.1:5454/', displayName = 'Greg')
        self.post = Mock(id = 'de305d54-75b4-431b-adb2-eb6b9e546015')
        self.comment = Comment().create_comment("Your pupper is wonderful", self.author)
        self.post.get_comments = MagicMock(return_value = ["Your pupper is wonderful"])

    @skip("get comment test")
    def test_get_comment(self):
        #call get comments from post object
        #check that they match
        mockGet = self.post.get_comments()
        self.assertEqual(mockGet, "APIPOINT")

    @skip("post comment test")
    def test_post_comment(self):
        #check post comment from post object
        comment="this is a comment"
        self.post.addComment(comment)
        #assume there is only one comment??
        self.assertEqual(comment,self.post.get_comments())
