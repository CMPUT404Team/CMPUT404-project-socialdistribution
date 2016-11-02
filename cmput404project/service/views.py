from django.contrib.auth.models import User, Group
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from models.Comment import Comment
from service.serializers import UserSerializer, GroupSerializer, AuthorSerializer, CommentSerializer
from models.Author import Author
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
    '''
    def get_object(self):
        return Comment.all()
    '''
    def get(self, request):
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
