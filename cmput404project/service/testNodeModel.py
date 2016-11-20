from django.test import TestCase
from models.Node import Node
from mock import MagicMock, Mock
from models.Author import Author
from django.contrib.auth.models import User
from unittest import skip

class NodeModelTests(TestCase):

    def setUp(self):
        su_username = "superuser"
        su_password = "test1234"
        remote_username = "testsuperuser"
        remote_password = "testpassword"
        superuser = User.objects.create_superuser(su_username, 'test@test.com', su_password)
        self.node = Node.create(
            displayName = "Home Node",
            baseUrl = "http://localhost:8000/",
            user = superuser,
            username = remote_username,
            password = remote_password 
            )
        self.node.save()

    def test_get_posts(self):
        posts = self.node.get_posts()
        print posts
        self.assertEqual([], posts)
