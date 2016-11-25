from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets,status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from django.utils.six import BytesIO
from models.Comment import Comment
from service.serializers import *
from models.Author import Author
from django.http import Http404
from models.Post import Post
from itertools import chain
from django.core import serializers
from django.urls import reverse
from django.forms import modelformset_factory
from django.shortcuts import render
from django.views.generic.edit import FormView
from AuthorForm import AuthorForm
from django.core.exceptions import SuspiciousOperation
from models.NodeManager import NodeManager
import json

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CommentAPIView(APIView):
    """
    API endpoint that allows the comments of a post to be viewed.


    Input: http://localhost:8000/posts/1dd49764-c855-4914-9785-508891598503/comments


    Output:


    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "author": {
                "url": "http://localhost:8000/author/f8c3b851-2e6a-44d1-b397-548a24b83f72/",
                "id": "f8c3b851-2e6a-44d1-b397-548a24b83f72",
                "displayName": "asdfg",
                "host": "asdf",
                "friends": []
            },
            "pubDate": "2016-11-16T21:40:56Z",
            "comment": "commmmmmm",
            "guid": "73f06229-395c-4bde-8058-fd3847133658"
        },
        {
            "author": {
                "url": "http://localhost:8000/author/f8c3b851-2e6a-44d1-b397-548a24b83f72/",
                "id": "f8c3b851-2e6a-44d1-b397-548a24b83f72",
                "displayName": "asdfg",
                "host": "asdf",
                "friends": []
            },
            "pubDate": "2016-11-16T23:28:33.066754Z",
            "comment": "",
            "guid": "ccfb10e5-b04b-46bd-8055-fa49a582e455"
        },
        {
            "author": {
                "url": "http://localhost:8000/author/f8c3b851-2e6a-44d1-b397-548a24b83f72/",
                "id": "f8c3b851-2e6a-44d1-b397-548a24b83f72",
                "displayName": "asdfg",
                "host": "asdf",
                "friends": []
            },
            "pubDate": "2016-11-16T23:34:47.129404Z",
            "comment": "",
            "guid": "ebcbda5b-afb3-4b13-b82b-8f29cb48e273"
        },
        {
            "author": {
                "url": "http://localhost:8000/author/f8c3b851-2e6a-44d1-b397-548a24b83f72/",
                "id": "f8c3b851-2e6a-44d1-b397-548a24b83f72",
                "displayName": "asdfg",
                "host": "asdf",
                "friends": []
            },
            "pubDate": "2016-11-16T23:47:23.826697Z",
            "comment": "",
            "guid": "41c28ee7-527a-4bd2-95b2-faed5a10fdde"
        }
    ]
    """
    def get_comments(self, postId):
        post = self.get_post(postId)
        comments = Comment.objects.filter(post_id = postId)
        return comments

    def get_author(self, authorId):
        try:
            author=Author.objects.get(id=authorId)
        except Author.DoesNotExist:
            raise Http404
        return author

    def get_post(self, postId):
        try:
            post=Post.objects.get(id=postId)
        except Post.DoesNotExist:
            raise Http404
        return post

    # TODO change to {comments: [...]}
    def get(self, request, pid):
        comments = self.get_comments(pid)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pid):
        post = self.get_post(pid)
        auth = self.get_author(request.data['comment']['author']['id'])
        try:
            comment = Comment.objects.get(guid=request.data['comment']['guid'])
            #comment already exists, update it
            serializer = CommentSerializerPost(comment, data=request.data['comment'])
        except Comment.DoesNotExist:
            #comment doesn't exist, create it
            serializer = CommentSerializerPost(data=request.data['comment'])

        if serializer.is_valid():
            serializer.save(post=post, author=auth)
            return Response({ "query": "addComment", "success":"true", "message":"Comment Added"})
        #print serializer.errors
        # TODO: change return to json success false
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorDetailView(APIView):
    '''
    Used to get the profile information of an author.

    Input: http://localhost:8000/author/f8c3b851-2e6a-44d1-b397-548a24b83f72/
    Output:

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "url": "http://localhost:8000/author/f8c3b851-2e6a-44d1-b397-548a24b83f72/",
        "id": "f8c3b851-2e6a-44d1-b397-548a24b83f72",
        "displayName": "asdfg",
        "host": "asdf",
        "friends": []
    }
    '''
    def get_object(self, uuid):
        try:
            return Author.objects.get(id=uuid)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, context={'request':request})
        return Response(serializer.data)

class PostsView(APIView):
    """
    Return a list of all public posts or create a new post \n\n

    Input: http://localhost:8000/posts/
    Output:

    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "title": "cd",
            "source": "sadf",
            "origin": "ds",
            "content": "",
            "contentType": "text/plain",
            "description": "",
            "author": {
                "url": "http://localhost:8000/author/f8c3b851-2e6a-44d1-b397-548a24b83f72/",
                "id": "f8c3b851-2e6a-44d1-b397-548a24b83f72",
                "displayName": "asdfg",
                "host": "asdf"
            },
            "count": 0,
            "size": 50,
            "next": "est",
            "published": "2016-11-16T21:37:02.127923Z",
            "id": "1dd49764-c855-4914-9785-508891598503",
            "visibility": "PUBLIC"
        }
    ]
    """
    def get(self, request):
        posts = Post.objects.all().filter(visibility="PUBLIC")
        for post in posts:
            comments = Comment.objects.filter(post_id=post.id)
            post.comments = comments
        serializer = PostSerializerGet(posts, many=True, context={'request':request})
        return Response({'posts':serializer.data})

    def post(self, request):
        serializer = PostSerializerPutPost(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostView(APIView):
    """
    Get, update or delete a particular post

    Input: http://localhost:8000/posts/1dd49764-c855-4914-9785-508891598503/
    Output:

    HTTP 200 OK
    Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "title": "cd",
        "source": "sadf",
        "origin": "ds",
        "content": "",
        "contentType": "text/plain",
        "description": "",
        "author": {
            "url": "http://localhost:8000/author/f8c3b851-2e6a-44d1-b397-548a24b83f72/",
            "id": "f8c3b851-2e6a-44d1-b397-548a24b83f72",
            "displayName": "asdfg",
            "host": "asdf"
        },
        "count": 0,
        "size": 50,
        "next": "est",
        "published": "2016-11-16T21:37:02.127923Z",
        "id": "1dd49764-c855-4914-9785-508891598503",
        "visibility": "PUBLIC"
    }
    """
    def get_object(self, uuid):
        try:
            return Post.objects.get(id=uuid)
        except Post.DoesNotExist:
            raise Http404
        except ValueError:
            raise ParseError("Malformed UUID")

    def get(self, request, pk):
        post = self.get_object(pk)
        comments = Comment.objects.filter(post_id=pk)
        post.comments = comments
        serializer = PostSerializerGet(post, context={'request':request})
        return Response(serializer.data)

    def post(self, request, pk):
        try:
            post = self.get_object(pk)
            serializer = PostSerializerPutPost(post, data=request.data, context={'request':request})
        except Http404:
            serializer = PostSerializerPutPost(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            post = self.get_object(pk)
            serializer = PostSerializerPutPost(post, data=request.data, context={'request':request})
        except Http404:
            serializer = PostSerializerPutPost(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VisiblePostsView(APIView):
    """
    Return a list of all posts available to the currently authenticated user

    Input: http://localhost:8000/author/posts/
    Output:

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "title": "cd",
            "source": "sadf",
            "origin": "ds",
            "content": "",
            "contentType": "text/plain",
            "description": "",
            "author": {
                "url": "http://localhost:8000/author/f8c3b851-2e6a-44d1-b397-548a24b83f72/",
                "id": "f8c3b851-2e6a-44d1-b397-548a24b83f72",
                "displayName": "asdfg",
                "host": "asdf"
            },
            "count": 0,
            "size": 50,
            "next": "est",
            "published": "2016-11-16T21:37:02.127923Z",
            "id": "1dd49764-c855-4914-9785-508891598503",
            "visibility": "PUBLIC"
        }
    ]
    """
    def get(self, request):
        posts = Post.objects.all()#.filter(visibility="?")
        for post in posts:
            comments = Comment.objects.filter(post_id=post.id)
            post.comments = comments
        serializer = PostSerializerGet(posts, many=True, context={'request':request})
        return Response({'posts':serializer.data})

class AuthorPostsView(APIView):
    """
    Return a list of available posts created by specified user

    GET Request object properties:
    request
    posts - the list of posts an author has
    uuid - author id
    """
    def get(self, request, pk):
        try:
            Author.objects.get(id=pk)
        except Author.DoesNotExist:
            raise Http404
        posts = Post.objects.all().filter(author__id=pk)
        for post in posts:
            comments = Comment.objects.filter(post_id=post.id)
            post.comments = comments
        serializer = PostSerializerGet(posts, many=True, context={'request':request})
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all()

class FriendDetailView(APIView):
    '''
    Used to determine whether two users are friends with eachother. This
    means that each user will have the other user in their friends list.

    GET Request object properties:
    request
    author1 - an object with the following properties:
         *uuid - author1 author id
         *host - author1 host
    author2 - an object with the following properties:
         *uuid - author2 author id
         *host - author2 host
    '''
    def get_object(self, uuid):
        try:
            return Author.objects.get(id=uuid)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, uuid1, uuid2):
        author1 = self.get_object(uuid1)
        author2 = self.get_object(uuid2)
        are_friends = author1.is_friend(author2)
        return Response({'query':'friends','authors': [str(uuid1), str(uuid2)], 'friends':are_friends})

    def delete(self, request, uuid1, uuid2):
        serializer = FriendRequestSerializer(request.data, data=request.data, context={'request':request})
        author = self.get_object(uuid1)
        friend = self.get_object(uuid2)
        author.friends.remove(friend)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MutualFriendDetailView(APIView):
    '''
    Used to list all the mutual friends between two authors. A post from an author
    will occur, with all their friends, and the uuid in the url will give the link
    of the friend to check it with.

    GET Response object properties:
    uuid1 - author1's uuid
    uuid2 - author2's uuid
    mutual_friends - the list of mutual friends both authors shares in common
    '''
    def post(self, request, uuid):
        serializer = FriendListSerializer(request.data, data=request.data, context={'request':request})
        mutual_friends = []
        if (serializer.is_valid(raise_exception=True)):
            author = self.get_object(serializer.validated_data['author'])
        author_all_friends = author.get_friends()
        friend_check = serializer.validated_data['authors']
        for friend in friend_check:
            if friend in author_all_friends:
                mutual_friends.append(friend)
                return Response({'query':'friends','author':author.id,'friends':mutual_friends})

    def get_object(self, uuid):
        try:
            return Author.objects.get(id=uuid)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        author = self.get_object(uuid)
        friends = author.get_friends()
        return Response({'query':'friends', 'friends':friends})

class FriendRequestView(APIView):
    '''
    Used to make a friend request.

    POST Request object properties:
    request
    author - an object with the following properties:
              * uuid - the author id
              * host - the author host
    friend - an object with the following properties:
             * uuid - the friend's author id
             * host - the friend's host
             * url - the url where friend is located
    POST Response object properties:
    Posting will manipulate the database, but not return any
    serialized data. A response of success will be returned
    on a successful request, the response will be an error
    message otherwise.
    '''
    def get_object(self, uuid):
        try:
            return Author.objects.get(id=uuid)
        except Author.DoesNotExist:
            raise Http404

    def post(self, request):
        serializer = FriendRequestSerializer(request.data,data=request.data, context={'request':request})
        if (serializer.is_valid(raise_exception=True)):
            author = self.get_object(serializer.validated_data['author']['id'])
            friend = self.get_object(serializer.validated_data['friend']['id'])
            author.add_friend(friend)
            return Response(status=204)

class PostsNodesView(APIView):
    """
    Return a list of all public posts from all Nodes
    """
    def get(self, request):
        posts = NodeManager.get_public_posts()
        return Response({'query':'frontend-posts', "posts":posts})

class VisiblePostsNodesView(APIView):
    """
    Return a list of all posts available to the currently authenticated users
    """
    def get(self, request):
        posts = NodeManager.get_posts()
        return Response({'query':'frontend-posts', "posts":posts})
