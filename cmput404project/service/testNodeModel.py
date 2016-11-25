from django.test import TestCase, LiveServerTestCase
from models.Node import Node
from models.NodeManager import NodeManager
from models.Author import Author
from models.Post import Post
from django.contrib.auth.models import User
from unittest import skip
from urlparse import urlparse
import json
import uuid
import base64

class NodeModelTests(LiveServerTestCase):

    def setUp(self):
        su_username = "superuser"
        su_password = "test1234"
        self.remote_username = "testsuperuser"
        self.remote_password = "testpassword"
        superuser = User.objects.create_superuser(username=su_username, email='test@test.com', password=su_password)
        superuser.save()
        remoteUser = User.objects.create_user(username=self.remote_username, password=self.remote_password)
        remoteUser.save()
        self.author = Author.create(host='local', displayName='testMonkey', user=superuser)
        self.author.save()
        self.parsed_test_url = urlparse(self.live_server_url)
        self.node = Node.create(
            displayName = "The Node",
            host = self.parsed_test_url.hostname+":"+str(self.parsed_test_url.port),
            path = "",
            user = remoteUser,
            username = self.remote_username,
            password = self.remote_password
            )
        self.node.save()

        self.nodemanager = NodeManager.create()
        self.nodemanager.save()
        self.create_post(self.author)

    def create_post(self, author):
        #create(cls, author,title,origin,description,categories,visibility):
        self.post = Post.create(author, "Yolo", "here", "Stuff", "Moar stuff", "PUBLIC")
        self.post.save()

    def test_node_creates_id(self):
        self.assertIsNotNone(self.node.id)

    def test_node_displayName_equal(self):
        self.assertEqual(self.node.displayName, "The Node")

    def test_node_host_equal(self):
        self.assertEqual(self.node.host, self.parsed_test_url.hostname+":"+str(self.parsed_test_url.port))

    def test_node_username_equal(self):
        self.assertEqual(self.node.username, self.remote_username)

    def test_node_password_equal(self):
        self.assertEqual(base64.b64decode(self.node.password), self.remote_password)

    def test_get_posts(self):
        posts = self.node.get_posts()
        self.assertEqual(str(self.post.id), posts[0]['id'])

    def test_get_posts_by_author(self):
        author_id = self.author.id
        posts = self.node.get_posts_by_author(author_id)
        #TODO test the contents of the object
        self.assertTrue(hasattr(posts, '__iter__'))

    def test_get_public_posts(self):
        posts = self.node.get_public_posts()
        self.assertEqual(str(self.post.id), posts['posts'][0]['id'])

    def test_get_nodes_from_nodemanager(self):
        nodes = self.nodemanager.get_nodes()
        #TODO test the contents of the object
        self.assertEqual(len(nodes), 1)
