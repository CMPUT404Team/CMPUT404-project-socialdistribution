from django.test import TestCase, LiveServerTestCase
from models.Node import Node
from models.NodeManager import NodeManager
from mock import MagicMock, Mock
from models.Author import Author
from models.Post import Post
from django.contrib.auth.models import User
from django.core.management import call_command
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
        self.author = Author.create(host=self.live_server_url, displayName='testMonkey', user=superuser)
        self.author.save()
        self.node = Node.create(
            displayName = "The Node",
            host = self.live_server_url,
            path = "",
            user = remoteUser,
            username = self.remote_username,
            password = self.remote_password
            )
        self.node.save()
        self.nodemanager = NodeManager.create()
        self.create_post(self.author)

    def create_post(self, author):
        #create(cls, author,title,origin,description,categories,visibility):
        self.post = Post.create(author, "Yolo", "here", "Stuff", "Moar stuff", "PUBLIC")
        self.post.save()

    def create_private_post(self, author):
        #create(cls, author,title,origin,description,categories,visibility):
        self.post = Post.create(author, "Private post", "here", "Secrets", "More secrets", "PRIVATE")
        self.post.save()

    def create_serveronly_post(self, author):
        #create(cls, author,title,origin,description,categories,visibility):
        self.post = Post.create(author, "ServerOnly post", "here", "Local secrets", "More local secrets", "SERVERONLY")
        self.post.save()

    def create_friend_post(self, author):
        self.post = Post.create(author, "friends post", "here", "friend secrets", "More friend secrets", "FRIENDS")
        self.post.save()

    def test_node_creates_id(self):
        self.assertIsNotNone(self.node.id)

    def test_node_displayName_equal(self):
        self.assertEqual(self.node.displayName, "The Node")

    def test_node_host_equal(self):
        self.assertEqual(self.node.host, self.live_server_url)

    def test_node_username_equal(self):
        self.assertEqual(self.node.username, self.remote_username)

    def test_node_password_equal(self):
        self.assertEqual(self.node.password, self.remote_password)

    def test_get_posts(self):
        posts = self.node.get_posts()
        self.assertEqual(str(self.post.id), posts['posts'][0]['id'])

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

    def test_befriend_remote_author(self):
        user = User.objects.create(username="hopefulFriend", password='superhopeful')
        friend = Author.create(host=self.live_server_url, displayName='hopefulFriend', user=user)
        friend.save()
        status = self.node.befriend(self.get_author_json(self.author), self.get_friend_json(friend))
        self.assertEqual(204, status)
        self.assertIn(friend, self.author.friends.all())

    def test_befriend_with_malformed_json(self):
        status = self.node.befriend({"this isn't the right json":"for making friends"}, {"Neither is":"this"})
        self.assertEqual(400, status)

    def test_befriend_with_friend_with_malformed_host(self):
         user = User.objects.create(username="hopefulFriendThatWillFail", password='superhopeful')
         friend = Author.create(host="NotAHostKnownByNodeManager.com", displayName='hopefulFriendThatWillFail', user=user)
         friend.save()
         http_response_code = self.nodemanager.befriend(self.get_author_json(self.author), self.get_friend_json(friend))
         self.assertEqual(404, http_response_code)

    def test_befriend_through_NodeManager(self):
        user = User.objects.create(username="hopefulFriend", password='superhopeful')
        friend = Author.create(host=self.live_server_url, displayName='hopefulFriend', user=user)
        friend.save()
        status = self.nodemanager.befriend(self.get_author_json(self.author), self.get_friend_json(friend))
        self.assertEqual(204, status)
        self.assertIn(friend, self.author.friends.all())

    def test_befriend_through_NodeManager_with_bad_json(self):
        status = self.node.befriend({"this isn't the right json":"for making friends"}, {"Neither is":"this"})
        self.assertEqual(400, status)

    def test_get_posts_by_friends(self):
        # Test for friends having multiple posts
        user1 = User.objects.create(username="hopefulFriend1", password='superhopeful1')
        friend1 = Author.create(host=self.live_server_url, displayName='hopefulFriend1', user=user1)
        friend1.save()
        self.author.add_friend(friend1)
        self.create_post(friend1)
        self.create_post(friend1)

        user2 = User.objects.create(username="hopefulFriend2", password='superhopeful2')
        friend2 = Author.create(host=self.live_server_url, displayName='hopefulFriend2', user=user2)
        friend2.save()
        self.author.add_friend(friend2)
        self.create_post(friend2)

        friend_ids = self.author.get_friends()
        posts = self.nodemanager.get_posts_by_friends(friend_ids)
        self.assertEqual(posts[0]['author']['displayName'], "hopefulFriend1")
        self.assertEqual(posts[2]['author']['displayName'], "hopefulFriend2")

    def test_get_posts_by_friends_fof(self):
        # Test for one friend having a post and friend of friend having a post
        user1 = User.objects.create(username="hopefulFriend", password='superhopeful')
        friend = Author.create(host=self.live_server_url, displayName='hopefulFriend', user=user1)
        friend.save()
        self.author.add_friend(friend)
        self.create_post(friend)

        user2 = User.objects.create(username="FriendOfFriend", password='superhopeful2')
        fof = Author.create(host=self.live_server_url, displayName='FriendOfFriend', user=user2)
        fof.save()
        friend.add_friend(fof)
        self.create_post(fof)

        friend_ids = self.author.get_friends()
        posts = self.nodemanager.get_posts_by_friends(friend_ids)
        self.assertEqual(posts[0]['author']['displayName'], "hopefulFriend")

    def test_get_posts_by_friends_without_posts(self):
        # Test for multiple friends having no posts
        user1 = User.objects.create(username="hopefulFriend1", password='superhopeful1')
        friend1 = Author.create(host=self.live_server_url, displayName='hopefulFriend1', user=user1)
        friend1.save()
        self.author.add_friend(friend1)

        user2 = User.objects.create(username="hopefulFriend2", password='superhopeful2')
        friend2 = Author.create(host=self.live_server_url, displayName='hopefulFriend2', user=user2)
        friend2.save()
        self.author.add_friend(friend2)

        friend_ids = self.author.get_friends()
        posts = self.nodemanager.get_posts_by_friends(friend_ids)
        self.assertEqual(posts, [])

    def test_get_author_posts_through_nodeManager_local_local_friend(self):
        #pass
        user = User.objects.create(username="user", password='dogs4lyf')
        friend = Author.create(host=self.live_server_url, displayName='friend1', user=user)
        friend.save()
        user2 = User.objects.create(username="user2", password='dogs4lyf')
        friend2 = Author.create(host=self.live_server_url, displayName='friend2', user=user2)
        friend2.save()
        friend2.add_friend(friend)
        friend.add_friend(friend2)
        self.create_friend_post(friend2)
        self.create_private_post(friend2)
        self.create_post(friend2)
        self.create_serveronly_post(friend2)
        stream = self.nodemanager.get_author_posts(friend.id, user2.id, self.live_server_url)
        #should see serveronly, public, friends. not private
    '''
    def test_get_author_posts_through_nodeManager_local_local_not_friend(self):
        pass

    def test_get_author_posts_through_nodeManager_local_remote_notfriend(self):
        pass

    def test_get_author_posts_through_nodeManager_user_is_author(self):
        pass
    '''

    def test_get_private_posts(self):
        self.create_private_post(self.author)
        self.create_post(self.author)
        self.create_private_post(self.author)
        posts = self.nodemanager.get_private_posts(self.author)
        self.assertEqual(posts[0]['visibility'], "PRIVATE")
        self.assertEqual(posts[1]['visibility'], "PRIVATE")

    def test_get_private_posts_empty(self):
        # Test for not displaying private posts of other users
        user = User.objects.create(username="hopefulSpy", password='superhopefulspy')
        spy = Author.create(host=self.live_server_url, displayName='hopefulSpy', user=user)
        spy.save()
        self.create_private_post(spy)
        posts = self.nodemanager.get_private_posts(self.author)
        self.assertEqual(posts, [])

    def test_get_serveronly_posts(self):
        self.create_serveronly_post(self.author)
        self.create_post(self.author)
        self.create_serveronly_post(self.author)
        posts = self.nodemanager.get_serveronly_posts(self.author)
        self.assertEqual(posts[0]['visibility'], "SERVERONLY")
        self.assertEqual(posts[1]['visibility'], "SERVERONLY")

    def test_get_serveronly_posts_empty(self):
        # Test for having no posts with visibility SERVERONLY
        posts = self.nodemanager.get_serveronly_posts(self.author)
        self.assertEqual(posts, [])

    def test_get_post_for_author(self):
        self.create_post(self.author)
        post = self.nodemanager.get_post_for_user(self.post.id, self.author)
        self.assertEqual(post['id'], str(self.post.id))


    def get_author_json(self, author):
        author_json = self.get_friend_json(author)
        author_json['url'] = author.host+"/author/"+str(author.id)
        return author_json

    def get_friend_json(self, friend):
        return {
                "id": str(friend.id),
                "host":friend.host,
                "displayName":friend.displayName
                }
        
    def test_get_Author_by_id(self):
        author = self.node.get_author(self.author.id)
        self.assertIsNotNone(author)
        self.assertEqual(author['id'], str(self.author.id))
        self.assertEqual(author['host'], self.author.host)
        self.assertEqual(author['displayName'], self.author.displayName)

    def test_get_Author_by_id_does_not_exist(self):
        author = self.node.get_author(uuid.uuid4()) 
        self.assertEqual(None, author)
