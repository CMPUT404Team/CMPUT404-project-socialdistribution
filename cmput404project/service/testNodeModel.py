from django.test import TestCase
from models.Node import Node
from models.NodeManager import NodeManager
from mock import MagicMock, Mock
from models.Author import Author
from django.contrib.auth.models import User
from unittest import skip
import base64

class NodeModelTests(TestCase):

    def setUp(self):
        su_username = "superuser"
        su_password = "test1234"
        self.remote_username = "testsuperuser"
        self.remote_password = "dGVzdHBhc3N3b3Jk" #testpassword
        superuser = User.objects.create_superuser(su_username, 'test@test.com', su_password)
        self.author = Author.create(host='local', displayName='testMonkey', user=superuser)
        self.node = Node.create(
            displayName = "The Node",
            baseUrl = "http://localhost:8000/", #needs to be changed to our actual server
            user = superuser,
            username = self.remote_username,
            password = self.remote_password 
            )
        self.node.save()

        self.nodemanager = NodeManager.create()
        self.nodemanager.save()

    def test_node_creates_id(self):
        self.assertIsNotNone(self.node.id)

    def test_node_displayName_equal(self):
        self.assertEqual(self.node.displayName, "The Node")

    def test_node_baseUrl_equal(self):
        self.assertEqual(self.node.baseUrl, "http://localhost:8000/")

    def test_node_username_equal(self):
        self.assertEqual(self.node.username, self.remote_username)

    def test_node_password_equal(self):
        self.assertEqual(self.node.password, self.remote_password)

    def test_get_posts(self):
        posts = self.node.get_posts()
        self.assertTrue(hasattr(posts, '__iter__'))

    def test_get_posts_by_author(self):
        author_id = self.author.id
        posts = self.node.get_posts_by_author(author_id)
        self.assertTrue(hasattr(posts, '__iter__'))

    def test_get_nodes_from_nodemanager(self):
        nodes = self.nodemanager.get_nodes()
        self.assertEqual(len(nodes), 1)
