from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from service.serializers import UserSerializer, GroupSerializer, PostSerializer
from django.http import Http404
from models.Post import Post

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

class PostsView(APIView):
    """
    Return a list of all posts or create a new post
    """
    def get(self, request):
        posts = Post.objects.all()
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
        serializer = PostSerializer(post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, uuid):
        post = self.get_object(uuid)
        serializer = PostSerializer(post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid):
        post = self.get_object(uuid)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    queryset = Post.objects.all()