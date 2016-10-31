from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets
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

class PostView(APIView):

    def get_object(self, uuid):
            try:
                    return Post.objects.get(id=uuid)
            except Post.DoesNotExist:
                    raise Http404

    def get(self, request, uuid):
            post = self.get_object(uuid)
            serializer = PostSerializer(post)
            return Response(serializer.data)
