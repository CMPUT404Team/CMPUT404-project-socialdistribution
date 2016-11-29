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
        if (friend_json):
            host = friend_json.get('host')
            if (Node.objects.filter(host__icontains=host).exists()):
                return Node.objects.get(host__startswith=host).befriend(author_json, friend_json)
        #We don't know about a host with that hostname, so we return not found
        return 404

    @classmethod
    def get_stream(self,user):
        stream=[]
        author=Author.objects.get(user_id=user.id)

        #get all public posts
        publicPosts=self.get_public_posts()
        for post in publicPosts:
            stream.append(post)

        #get all posts from friends of user
        friends=author.get_friends()
        friendPosts=self.get_posts_by_friends(friends)
        for post in friendPosts:
            if post not in stream:
                stream.append(post)

        #get user private posts
        private=self.get_private_posts(author)
        for post in private:
            stream.append(post)
        return stream


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
    def get_author(self, author_id):
        for node in self.get_nodes():
            author = node.get_author(author_id)
            if (author != None):
                return author

    @classmethod # add FOAF if our endpoint works
    #host is the host of user
    def get_author_posts(self, id, user_id, host):
        stream = []
        friends = True
        local = False
        nodes = self.get_nodes()
        #assumes the user has an author - won't work otherwise
        user_auth = Author.objects.get(user_id=user_id)
        node = None

        try:
            author = Author.objects.get(id=id)
            local = True if author.host == "http://"+host else False
        except Author.DoesNotExist:
            friends = False
            author = None

        #a user can see their own posts
        if (local and str(id) == str(user_auth.id)):
            return Post.objects.filter(author_id=user_auth.id)

        #find node
        if (author == None):
            #find the author's host and node
            for n in nodes:
                try:
                    url = n.get_base_url()+'/author/'+str(id)
                    json_data = n.get_json(url)
                    # is this the author's host?
                    if (json_data['host'] == n.host):
                        node = n
                        break;
                except:
                    pass
            if (node == None):
                raise Exception("Author doesn't exist anywhere!")
        #already know host, find the node
        else:
            if (Node.objects.filter(host__icontains=author.host).exists()):
                node = Node.objects.get(host__startswith=author.host)

        #check if id and user are friends
        if (friends):
            #see if can find author in friends list of user
            # user is not friends with that author
            if author not in user_auth.friends.all():
                friends = False
            # user is friends, but is it mutal?
            else:
                # check if friends friends/<authorid1>/<authorid2>
                friends = node.are_friends(id, user_auth.id)

        posts = node.get_posts_by_author(id)
        for p in posts['posts']:
            if (local and p['visibility'] == 'SERVERONLY'):
                # add serveronly posts
                stream.append(p)
            elif (friends and p['visibility'] == 'FRIENDS'):
                # add friend posts
                stream.append(p)
            elif (p['visibility'] == 'PUBLIC'):
                stream.append(p)
        return stream

    @classmethod
    def get_post_by_postid(self, post_id):
        nodes = self.get_nodes()
        for node in nodes:
            jsonData = node.get_post(post_id)
            if (jsonData == None):
                continue
            else:
                # need to account for diferrent format of single post endpoint
                if 'posts' in jsonData:
                    return jsonData['posts'][0]
                else:
                    return jsonData
        return 404

    @classmethod
    def check_post_auth(self, post, author):
        post_author_id = post['author']
        visibility = post['visibility']
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
