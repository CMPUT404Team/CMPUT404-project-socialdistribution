from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseNotModified
from django.urls import reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.views import APIView
import urllib2, base64, json, os
from django.template.response import TemplateResponse
from django.conf import settings
from models.Author import Author
from models.NodeManager import NodeManager
from models.FriendRequest import FriendRequest
from . import views
from django.views.generic.edit import FormView
from rest_framework.response import Response
from AuthorForm import AuthorForm
from serializers import AuthorSerializer
import ast
import uuid

def index(request):
    return redirect("author-add")

def get_author_object(user):
    try:
        return Author.objects.get(user=user)
    except Author.DoesNotExist:
        raise Http404

class PostView(APIView):
    '''
    '''
    def get(self, request, pk):
        post = views.PostView.as_view()(request, pk).data
        return render(request, "posts-id.html", {"post":post})

class CommentsView(APIView):
    '''
    '''
    def get(self, request, pk):
        comments = views.CommentAPIView.as_view()(request, pk).data
        post = views.PostView.as_view()(request, pk).data
        return render(request, "posts-id-comments.html", {"comments": comments, "host": request.get_host(), "post": post})

class PostsView(APIView):
    '''
    '''
    def get(self, request):
        response = views.PostsView.as_view()(request)
        if (response.status_code == 200):
            return render(request, "posts.html", {"posts":response.data['posts']})
        else:
            return HttpResponse(status=response.status_code)

class AuthorCreateView(FormView):
    template_name = "author_form.html"
    form_class = AuthorForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.create_author(self.request.get_host())
        self.success_url = reverse('awaiting-approval')
        return super(AuthorCreateView, self).form_valid(form)

class AuthorPostsView(APIView):
    '''
    '''
    def get(self, request):
        posts = NodeManager.get_stream(request.user)
        return render(request, "author-posts.html", {"posts":posts})

class AuthorIdPostsView(APIView):
    '''
    '''
    def get(self, request, pk):
        posts =  views.AuthorPostsView.as_view()(request, pk).data
        author = views.AuthorDetailView.as_view()(request, pk).data
        return render(request, "author-id-posts.html", {"posts":posts, "host":request.get_host(), "author": author })

class AuthorDetailView(APIView):
    '''
    '''
    def get(self, request, pk):
        author = NodeManager.get_author(pk)
        currently_friends = get_author_object(request.user).is_following(author['id'])
        friends = []
        for friend in author["friends"]:
            f = views.AuthorDetailView.as_view()(request, friend["id"]).data
            friends.append(f)
        return render(request, "author-id.html", {"author": author, "friends": friends, "currently_friends":currently_friends})

class FriendView(APIView):
    def get(self, request):
        author = views.AuthorDetailView.as_view()(request, pk).data
        friends = []
        for friend in author["friends"]:
            f = views.AuthorDetailView.as_view()(request, friend["id"]).data
            friends.append(f)
        return render(request, "friends.html", {"friends":friends})

class BefriendView(APIView): 

    def post(self, request, pk):
        author = get_author_object(request.user) 
        author_json = AuthorSerializer(author, context={'request':request}).data
        friend_json = NodeManager.get_author(pk)
        if (friend_json == None):
            return Response(status=404)
        status_code = NodeManager.befriend(author_json, friend_json)
        if (str(status_code).startswith('2')):
            return redirect('frontend-author-detail', pk) 
        return Response(status=status_code)

class UnfriendView(APIView):

    def post(self, request, pk):
        author = get_author_object(request.user)
        author.remove_friend(Author.objects.get(id=pk))
        return redirect('frontend-author-detail', pk)
        

class FriendRequestsView(APIView):

    def get(self, request):
        #based on the currently logged in user, display the friend requests
        friend_requests = Author.objects.get(user_id=request.user.id).friendrequest_set.all()
        return render(request, 'friend-requests.html', {"requests":friend_requests})

class FriendRequestsAddView(APIView):

    def post(self, request, pk):
        #Create author object of the friend
        serializer = AuthorSerializer(data=NodeManager.get_author(pk), context={'request':request})
        if(serializer.is_valid(raise_exception=True)):
            friend = serializer.save()
            author = Author.objects.get(user=request.user)
            author.add_friend(friend)
            FriendRequest.objects.get(requesting_author_id=pk, author=author).delete()
            return redirect('friend-requests')

class FriendRequestsRemoveView(APIView):

    def post(self, request, pk):
        FriendRequest.objects.get(requesting_author_id=pk, author=Author.objects.get(user=request.user)).delete()
        return redirect('friend-requests')
