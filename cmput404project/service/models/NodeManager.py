from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse
from Author import Author
from Node import Node
from Post import Post
import uuid, json, requests

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
    def get_author_posts(self, id, user):
        stream = []
        try:
            author = Author.objects.get(id=id)
            local = True if author.host == request.get_host() else False
            # if they are the same person they can see private posts
            if (id == user):
                stream = Post.objects.filter(author=local, visibility="PRIVATE")
            #check if friends, then get friend posts if they are

            requests.get(url, auth=(self.username,self.password))
            views.FriendDetailView.as_view(request, )
            if (friends)

        except Author.DoesNotExist:
            #local = None
            nodes = self.get_nodes()
            for node in nodes:
                '''
                for each node get:
                    - private if they are the same author
                    - all friend posts if id and user are friends
                    - public posts of that id
                    - serveronly if on our server
                    - (FOAF posts)
                    - (posts for that user)
                '''
                pass
            pass
        return stream
