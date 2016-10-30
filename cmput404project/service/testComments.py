from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.urls import reverse
from rest_framework import status
from .views import UserViewSet
from mock import MagicMock, Mock
from datetime import datetime
from .models import Comment

class CommentUnitTest():

    def published_recently(self, pubDate, now):
        if (now.day == pubDate.day):
            return True
        else:
            return False

    def test_create_comment(self):
        author = Mock(id = 'de305d54-75b4-431b-adb2-eb6b9e546013', host = 'http://127.0.0.1:5454/', displayName = 'Greg')
        pubDate = datetime.now()
        comment = 'This is a comment'
        guid = uuid4.uuid()
        comm = Comment().create_comment(comment, author)
        assertEqual(comm.author, author, "Author not equal")
        assertEqual(comm.comment, comment, "Comment not equal")
        assertIsInstance(comm.pubDate, datetime, "Not a datetime object")
        assertTrue(self.published_recently(comm.pubDate), "Date not recent enough")
        assertIsInstance(comm.guid, uuid4, "Not a uuid object")
        assertIsInstance(comm, Comment, "Not a comment object")

class CommentViewSetTests(APITestCase):

    def setUp(self):
        superuser = User.objects.create_superuser('superuser', 'test@test.com', 'test1234')
        self.client = APIClient()
        #Authenticate as a super user so we can test everything
        self.client.force_authenticate(user=superuser)
        self.author = Mock(id = 'de305d54-75b4-431b-adb2-eb6b9e546013', host = 'http://127.0.0.1:5454/', displayName = 'Greg')
        self.post = Mock(id = 'de305d54-75b4-431b-adb2-eb6b9e546015')
        self.comment = Comment().create_comment("Your pupper is wonderful", author)
        self.post.get_comments = MagicMock(return_value = ["Your pupper is wonderful"])

    def test_get_comment(self):
        #call get comments from post object
        #check that they match
        mockGet = self.post.get_comments()
        self.assertEqual(mockGet, "APIPOINT")

    def test_post_comment(self):
        #check post comment from post object
        pass
