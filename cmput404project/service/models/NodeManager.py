from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse
from Author import Author
from Node import Node
from Post import Post
import uuid, json

class NodeManager():
    @classmethod
    def create(cls):
        return cls()

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(NodeManager, self).save(*args, **kwargs)

    @classmethod
    def concatJson(self, json1, json2):
        jsonConc = {key: value for (key, value) in (json1.items() + json2.items())}
        #jsonConc = json.dumps(jsonConc)
        return jsonConc

    @classmethod
    def get_nodes(self):
        nodes = Node.objects.all()
        return nodes

    @classmethod
    def get_public_posts(self):
        stream = []
        nodes = self.get_nodes()
        for node in nodes:
            jsonData = node.get_public_posts()
            if (jsonData == None):
                continue
            i = 0
            for post in jsonData['posts']:
                stream.append(jsonData['posts'][i])
                i+=1
        return stream

    @classmethod
    def get_posts(self):
        stream = []
        nodes = self.get_nodes()
        for node in nodes:
            jsonData = node.get_posts()
            if (jsonData == None):
                continue
            i = 0
            for post in jsonData['posts']:
                stream.append(jsonData['posts'][i])
                i+=1
        return stream

    @classmethod
    def befriend(self, author_json, friend_json):
        host = friend_json.get('host')
        if (Node.objects.filter(host__icontains=host).exists()):
            return Node.objects.get(host__startswith=host).befriend(author_json, friend_json)
        else:
            #We don't know about a host with that hostname, so we return not found
            return 404

    @classmethod
    def get_posts_by_friends(self, author_ids):
        stream = []
        nodes = self.get_nodes()
        for author_id in author_ids:
            for node in nodes:
                jsonData = node.get_posts_by_author(author_id)
                if (jsonData == None):
                    continue
                i = 0
                for post in jsonData['posts']:
                    stream.append(jsonData['posts'][i])
                    i+=1
        return stream

    @classmethod
    def get_private_posts(self, author):
        posts = Post.objects.all().filter(author=author, visibility="PRIVATE")
        posts_list = list(posts.values())
        return posts_list

    @classmethod
    def get_serveronly_posts(self, author):
        posts = Post.objects.all().filter(author=author, visibility="SERVERONLY")
        posts_list = list(posts.values())
        return posts_list

    @classmethod
    def get_post_by_postid(self, post_id):
        post_queryset = Post.objects.filter(id=post_id)
        if not post_queryset:
            nodes = self.get_nodes()
            for node in nodes:
                jsonData = node.get_post(post_id)
                if (jsonData == None):
                    continue
                else:
                    return jsonData
            return 404
        else:
            post = post_queryset.values()
            return post

    @classmethod
    def check_post_auth(self, post, author):
        post_author_id = post.author.id
        visibility = post.visibility
        if author.id == post_author_id:
            return True
        elif visibility == "PUBLIC":
            return True
        elif visibility == "Friend":
            is_friend = author.is_friend(post.author)
            if is_friend:
                return True
        elif visibility == "SERVERONLY":
            if post.author.host == author.host:
                return True
        return False

    @classmethod
    def get_post_for_user(self, post_id, author):
        post = self.get_post_by_postid(post_id)
        if post == 404:
            return 404
        else:
            is_authorized = self.check_post_auth(post, author)
            if not is_authorized:
                return 404
        return post