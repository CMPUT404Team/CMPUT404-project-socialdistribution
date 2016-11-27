from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse
from Author import Author
from Node import Node
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
        print "friend json", friend_json
        if (friend_json):
            host = friend_json.get('host')
            if (Node.objects.filter(host__icontains=host).exists()):
                return Node.objects.get(host__startswith=host).befriend(author_json, friend_json)
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
