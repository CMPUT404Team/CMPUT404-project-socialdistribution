from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from models.Comment import Comment
from service.serializers import UserSerializer, GroupSerializer, AuthorSerializer, CommentSerializer, PostSerializer
from models.Author import Author
from models.Post import Post
from itertools import chain
from django.core import serializers
from django.http import Http404


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
    def get(self, request, id):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class AuthorDetailView(APIView):

	def get_object(self, uuid):
        	try:
            		return Author.objects.get(id=uuid)
        	except Author.DoesNotExist:
            		raise Http404

	def get(self, request, uuid):
        	author = self.get_object(uuid)
        	serializer = AuthorSerializer(author)
        	return Response(serializer.data)
class PostsView(APIView):
    """
    Return a list of all public posts or create a new post
    """
    def get(self, request):
        posts = Post.objects.all().filter(visibility="PUBLIC")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
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

    def get(self, request, uuid):
        post = self.get_object(uuid)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def post(self, request, uuid):
        post = self.get_object(uuid)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, uuid):
        post = self.get_object(uuid)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        post = self.get_object(uuid)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class VisiblePostsView(APIView):
    """
    Return a list of all posts available to the currently authenticated user
    """
    def get(self, request):
        posts = Post.objects.all()#.filter(visibility="?")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class AuthorPostsView(APIView):
    """
    Return a list of available posts created by specified user
    """
    def get(self, request):
        posts = Post.objects.all()#.filter(author.id="?")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all()
