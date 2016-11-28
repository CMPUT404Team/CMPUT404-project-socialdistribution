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

    @classmethod # add FOAF if our endpoint works
    def get_author_posts(self, id, user):
        stream = []
        friends = True
        local = False
        nodes = self.get_nodes()
        print type(user)

        try:
            author = Author.objects.get(id=id)
            local = True if author.host == request.get_host()# else False
        except Author.DoesNotExist:
            friends = False
            author = None

        #a user can see their own private posts
        if (local and id == user):
                private = Post.objects.filter(author=author, visibility="PRIVATE")
                for post in private:
                    stream.append(post)

        if (author == None):
            #find the author's host
            for node in nodes:
                try:
                    url = node.get_base_url()+'/author/'
                    print url
                    #requests.get(url, auth=(self.username,self.password))
                    json_data = node.make_authenticated_request(url)
                    # TODO: find result of json_data
                except:
                    pass

        #check if id and user are friends
        if (friends):
            #see if can find author in friends list of user
            user_auth = Author.objects.get(id=user)
            # user is not friends with that author
            if author not in user_auth.friends:
                friends = False
            # user is friends, but is it mutal?
            else:
                # TODO
                #do remote query for friends - have host
                # TODO: set friends based on json result
                pass

        # TODO
        # query /author/posts
        # sort
        # add posts marked public
        # if local : add posts marked server only
        # if friends: add posts marked friends

        return stream
