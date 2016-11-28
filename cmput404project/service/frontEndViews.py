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
from models.NodeManager import NodeManager
from . import views
from django.views.generic.edit import FormView
from rest_framework.response import Response
from AuthorForm import AuthorForm

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
        author = views.AuthorDetailView.as_view()(request, pk).data
        friends = []
        print author
        for friend in author["friends"]:
            f = views.AuthorDetailView.as_view()(request, friend["id"]).data
            print f
            friends.append(f)
        return render(request, "author-id.html", {"author": author, "friends": friends, "host": request.get_host()})

class FriendView(APIView):
    def get(self, request):
        author = views.AuthorDetailView.as_view()(request, pk).data
        friends = []
        for friend in author["friends"]:
            f = views.AuthorDetailView.as_view()(request, friend["id"]).data
            friends.append(f)
        return render(request, "friends.html", {"friends":friends})
