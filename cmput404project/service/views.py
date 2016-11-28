from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets,status
from rest_framework.parsers import JSONParser
from rest_framework.pagination import PageNumberPagination
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
from django.core.paginator import Paginator
from django.urls import reverse
from django.forms import modelformset_factory
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.http.request import QueryDict
from AuthorForm import AuthorForm
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


    Input: http://localhost:8000/posts/ea8c25f6-35d6-4918-8232-e6df8e697424/comments

    Output:

    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
			"author": {
				"url": "http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/",
				"id": "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
				"displayName": "asdf",
				"host": "a",
				"friends": []
            },
            "pubDate": "2016-11-26T02:08:42Z",
            "comment": "First Comment!!",
            "guid": "db42e75f-4045-415a-8969-f8601360981a"
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

    def get(self, request, pid):
        comments = self.get_comments(pid)
        paginator = CustomPagination()
        paginator.paginate_queryset(comments, request)
        paginator.page_size = request.GET['size'] if 'size' in request.GET else paginator.page_size
        comments = paginator.page.object_list
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data, 'comments', 'comments',
                    request.GET['size'] if 'size' in request.GET else None)

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

    Input: http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/
    Output:

    HTTP 200 OK
	Allow: GET, HEAD, OPTIONS
	Content-Type: application/json
	Vary: Accept

    {
        "url": "http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/",
        "id": "f6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
        "displayName": "asdf",
        "host": "a",
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
    Return a list of all public posts or create a new post 

    Input: http://localhost:8000/posts/
    Output:

    HTTP 200 OK
	Allow: GET, POST, HEAD, OPTIONS
	Content-Type: application/json
	Vary: Accept

	{
    	"posts": [
    	    {
    	        "title": "My New Post",
    	        "source": "na",
    	        "origin": "na",
    	        "content": "",
    	        "contentType": "text/plain",
    	        "description": "",
    	        "author": {
    	            "url": "http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/",
    	            "id": "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
    	            "displayName": "asdf",
    	            "host": "a"
    	        },
    	        "count": 0,
    	        "size": 50,
    	        "next": "na",
    	        "comments": [
    	            {
    	                "author": {
    	                    "url": "http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b2	2b27d9c3/",
    	                    "id": "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
    	                    "displayName": "asdf",
    	                    "host": "a",
    	                    "friends": []
    	                },
    	                "pubDate": "2016-11-26T02:08:42Z",
    	                "comment": "First Comment!!",
    	                "guid": "db42e75f-4045-415a-8969-f8601360981a"
    	            }
    	        ],
    	        "published": "2016-11-26T02:00:44.793165Z",
    	        "id": "ea8c25f6-35d6-4918-8232-e6df8e697424",
    	        "visibility": "PUBLIC"
    	    }
    	]
	}
    """

    def get(self, request):
        posts = Post.objects.all().filter(visibility="PUBLIC")
        paginator = CustomPagination()
        paginator.paginate_queryset(posts, request)
        paginator.page_size = request.GET['size'] if 'size' in request.GET else paginator.page_size
        posts = paginator.page.object_list
        serializer = PostSerializerGet(posts, many=True, context={'request':request})
        cip = PaginationOfCommentInPost()
        data = cip.add_to_post(serializer.data, request)
        return paginator.get_paginated_response(data, 'posts', 'posts',
                request.GET['size'] if 'size' in request.GET else None)

    def post(self, request):
        serializer = PostSerializerPutPost(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    """
    Get, update or delete a particular post

    Input: http://localhost:8000/posts/ea8c25f6-35d6-4918-8232-e6df8e697424/
    Output:

	HTTP 200 OK
	Allow: GET, POST, PUT, DELETE, HEAD, OPTIONS
	Content-Type: application/json
	Vary: Accept

    
	{
	    "title": "My New Post",
	    "source": "na",
	    "origin": "na",
	    "content": "",
	    "contentType": "text/plain",
	    "description": "",
	    "author": {
	        "url": "http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/",
	        "id": "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
	        "displayName": "asdf",
	        "host": "a"
	    },
	    "count": 0,
	    "size": 50,
	    "next": "na",
	    "comments": [
	        {
	            "author": {
	                "url": "http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/",
	                "id": "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
	                "displayName": "asdf",
	                "host": "a",
	                "friends": []
	            },
	            "pubDate": "2016-11-26T02:08:42Z",
	            "comment": "First Comment!!",
	            "guid": "db42e75f-4045-415a-8969-f8601360981a"
	        }
	    ],
	    "published": "2016-11-26T02:00:44.793165Z",
	    "id": "ea8c25f6-35d6-4918-8232-e6df8e697424",
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
        post = [self.get_object(pk)]
        comments = Comment.objects.filter(post_id=uuid.UUID(pk))
        post[0].comments = comments
        paginator = CustomPagination()
        paginator.paginate_queryset(post, request)
        paginator.page_size = request.GET['size'] if 'size' in request.GET else paginator.page_size
        post = paginator.page.object_list
        serializer = PostSerializerGet(post, many=True, context={'request':request})
        cip = PaginationOfCommentInPost()
        data = cip.add_to_post(serializer.data, request)
        return paginator.get_paginated_response(data, 'posts', 'posts',
                request.GET['size'] if 'size' in request.GET else None)

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
        if (request.user == post.author.user):
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class VisiblePostsView(APIView):
    """
    Return a list of all posts available to the currently authenticated user

    Input: http://localhost:8000/author/posts/
    Output:

    HTTP 200 OK
	Allow: GET, HEAD, OPTIONS
	Content-Type: application/json
	Vary: Accept

	{
    	"posts": [
    	    {
    	        "title": "My New Post",
    	        "source": "na",
    	        "origin": "na",
    	        "content": "",
    	        "contentType": "text/plain",
    	        "description": "",
    	        "author": {
    	            "url": "http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/",
    	            "id": "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
    	            "displayName": "asdf",
    	            "host": "a"
    	        },
    	        "count": 0,
    	        "size": 50,
    	        "next": "na",
    	        "comments": [
    	            {
    	                "author": {
    	                    "url": "http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/",
        	                "id": "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
        	                "displayName": "asdf",
        	                "host": "a",
        	                "friends": []
        	            },
        	            "pubDate": "2016-11-26T02:08:42Z",
        	            "comment": "First Comment!!",
        	            "guid": "db42e75f-4045-415a-8969-f8601360981a"
        	        }
        	    ],
        	    "published": "2016-11-26T02:00:44.793165Z",
        	    "id": "ea8c25f6-35d6-4918-8232-e6df8e697424",
        	    "visibility": "PUBLIC"
        	}
    	]
	}
    """
    def get(self, request):
        posts = Post.objects.all().exclude(visibility="PRIVATE").exclude(visibility="SERVERONLY")
        for post in posts:
            comments = Comment.objects.filter(post_id=post.id)
            post.comments = comments
        paginator = CustomPagination()
        paginator.paginate_queryset(posts, request)
        paginator.page_size = request.GET['size'] if 'size' in request.GET else paginator.page_size
        posts = paginator.page.object_list
        serializer = PostSerializerGet(posts, many=True, context={'request':request})
        cip = PaginationOfCommentInPost()
        data = cip.add_to_post(serializer.data, request)
        return paginator.get_paginated_response(data, 'posts', 'posts',
                request.GET['size'] if 'size' in request.GET else None)

class AuthorPostsView(APIView):
    """
    Return a list of available posts created by specified user

    Input: http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/posts/
	output: 

	HTTP 200 OK
	Allow: GET, HEAD, OPTIONS
	Content-Type: application/json
	Vary: Accept

	[
    	{
    	    "title": "My New Post",
    	    "source": "na",
    	    "origin": "na",
    	    "content": "",
    	    "contentType": "text/plain",
    	    "description": "",
    	    "author": {
    	        "url": "http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/",
    	        "id": "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
    	        "displayName": "asdf",
    	        "host": "a"
    	    },
    	    "count": 0,
    	    "size": 50,
    	    "next": "na",
    	    "comments": [
    	        {
    	            "author": {
    	                "url": "http://localhost:8000/author/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/",
    	                "id": "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
    	                "displayName": "asdf",
    	                "host": "a",
    	                "friends": []
    	            },
    	            "pubDate": "2016-11-26T02:08:42Z",
    	            "comment": "First Comment!!",
    	            "guid": "db42e75f-4045-415a-8969-f8601360981a"
    	        }
    	    ],
    	    "published": "2016-11-26T02:00:44.793165Z",
    	    "id": "ea8c25f6-35d6-4918-8232-e6df8e697424",
    	    "visibility": "PUBLIC"
    	}
	]
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
        paginator = CustomPagination()
        paginator.paginate_queryset(posts, request)
        paginator.page_size = request.GET['size'] if 'size' in request.GET else paginator.page_size
        posts = paginator.page.object_list
        serializer = PostSerializerGet(posts, many=True, context={'request':request})
        cip = PaginationOfCommentInPost()
        data = cip.add_to_post(serializer.data, request)
        return paginator.get_paginated_response(serializer.data, 'posts', 'posts',
                request.GET['size'] if 'size' in request.GET else None)

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all()

class FriendDetailView(APIView):
    '''
    Used to determine whether two users are friends with eachother. This
    means that each user will have the other user in their friends list.

    Input: http://localhost:8000/friends/6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3/3c1f82f3-e207-48bb-9849-a9b03f3bfb96
    Output:
    HTTP 200 OK
	Allow: GET, HEAD, OPTIONS
	Content-Type: application/json
	Vary: Accept

	{
    	"query": "friends",
    	"friends": true,
    	"authors": [
    	    "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3",
    	    "3c1f82f3-e207-48bb-9849-a9b03f3bfb96"
    	]
	}
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

class MutualFriendDetailView(APIView):
    '''
    Used to list all the mutual friends between two authors. A post from an author
    will occur, with all their friends, and the uuid in the url will give the link
    of the friend to check it with.

	Input: http://localhost:8000/friends/3c1f82f3-e207-48bb-9849-a9b03f3bfb96/
	Output:
    
	HTTP 200 OK
	Allow: GET, POST, HEAD, OPTIONS
	Content-Type: application/json
	Vary: Accept

	{
    	"query": "friends",
    	"friends": [
    	    "6384edbd-27bb-4ee5-9ac6-e2b22b27d9c3"
    	]
	}
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
    query
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

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'

    def get_paginated_response(self, data, data_field, query, size = None):
        if (size == None):
            size = self.page_size
        result = {
            'query': query,
            'count': self.page.paginator.count,
            'size': size,
            data_field: data
        }
        if self.page.has_next():
            result['next'] = self.get_next_link()
        if self.page.has_previous():
            result['previous'] = self.get_previous_link()

        return Response(result)

class PaginationOfCommentInPost():

    def add_to_post(self, data, request):
        #make a copy of the request without the query params
        r = request
        r.GET = QueryDict('')
        i = 0
        for p in data:
            response = CommentAPIView.as_view()(r, pid=p['id'])
            for field in response.data:
                f = ['comments', 'count', 'size', 'previous', 'next']
                if (field in f):
                    data[i][field] = response.data[field]
            i += 1
        return data
