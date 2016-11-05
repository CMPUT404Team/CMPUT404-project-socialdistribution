from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from service.serializers import *
from models.Author import Author
from django.http import Http404
from django.forms import modelformset_factory
from django.shortcuts import render
from django.views.generic.edit import FormView
from AuthorForm import AuthorForm

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
