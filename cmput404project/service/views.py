from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets,status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.six import BytesIO
from models.Comment import Comment
from service.serializers import *
from models.Author import Author
from django.http import Http404
from models.Post import Post
from itertools import chain
from django.core import serializers
from django.forms import modelformset_factory
from django.shortcuts import render
from django.views.generic.edit import FormView
from AuthorForm import AuthorForm
from django.core.exceptions import SuspiciousOperation
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
    """
    def get_comments(self, postId):
        comments = Comment.objects.filter(post_id = postId)
        if not comments:
            raise Http404
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
    """
    def get(self, request):
        posts = Post.objects.all().filter(visibility="PUBLIC")
        serializer = PostSerializer(posts, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostView(APIView):
    """
    Get, update or delete a particular post
    """
    def get_object(self, uuid):
        try:
            return Post.objects.get(id=uuid)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, context={'request':request})
        return Response(serializer.data)

    def post(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, context={'request':request})
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
    """
    def get(self, request):
        posts = Post.objects.all()#.filter(visibility="?")
        serializer = PostSerializer(posts, many=True, context={'request':request})
        return Response(serializer.data)

class AuthorPostsView(APIView):
    """
    Return a list of available posts created by specified user
    """
    def get(self, request):
        posts = Post.objects.all()#.filter(author.id="?")
        serializer = PostSerializer(posts, many=True, context={'request':request})
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

class AuthorCreate(FormView):
    template_name = "author_form.html"
    form_class = AuthorForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        self.success_url = form.create_author(self.request.get_host())
        return super(AuthorCreate, self).form_valid(form)
