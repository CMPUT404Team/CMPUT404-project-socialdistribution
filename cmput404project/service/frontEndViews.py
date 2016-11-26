from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import TemplateHTMLRenderer
import urllib2, base64, json, os
from rest_framework.views import APIView
from django.template.response import TemplateResponse
from django.conf import settings
from models.Author import Author
from . import views

def index(index):
    return redirect("author-add")

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
            return render(request, "posts.html", {"posts":response.data['posts'], "host": request.get_host()})
        else:
            return HttpResponse(status=response.status_code)

class AuthorPostsView(APIView):
    '''
    '''
    def get(self, request):
        response = views.VisiblePostsNodesView.as_view()(request) 
        posts = response.data['posts']
        return render(request, "author-posts.html", {"posts":posts})

class AuthorIdPostsView(APIView):
    '''
    '''
    def get(self, request, pk):
        posts =  views.AuthorPostsView.as_view()(request, pk).data 
        author = views.AuthorDetailView.as_view()(request, pk).data
        return render(request, "author-id-posts.html", {"posts":posts, "host":request.get_host(), "author": author })

class FriendView(APIView):
    def get(self, request):
        #author = Author.objects.filter(user_id = request.user.id)[0]
        friends = views.MutualFriendDetailView.as_view()(request).data
        return render(request, "friends.html", {"friends":friends})
