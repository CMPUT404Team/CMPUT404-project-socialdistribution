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
from AuthorExistsForm import AuthorExistsForm
from LoginForm import LoginForm
from CommentForm import CommentForm
from PostForm import PostForm
from serializers import AuthorSerializer
import ast
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
import uuid

def index(index):
    return redirect("home")

def get_author_exists(username):
    return User.objects.filter(username=username).exists()

def get_author_object(user):
    try:
        return Author.objects.get(user=user)
    except Author.DoesNotExist:
        raise Http404

class HomeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        print request.user.is_authenticated
        if not request.user.is_authenticated:
            form = AuthorExistsForm()
            return render(request, 'home.html', {'form': form})
        else:
            form = AuthorExistsForm()
            return render(request, 'home.html', {'form': form})

class AuthorExistsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        form = LoginForm()
        return redirect("login")

    def post(self, request):
        self.username = request.POST['displayName']
        user_exists = get_author_exists(self.username)
        if user_exists:
            return redirect("login")
        else:
            return redirect("author-add")

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        username = request.POST['displayName']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("welcome")
        else:
            return redirect("login")

class WelcomeView(APIView):

    def get(self, request):
        author = get_author_object(request.user)
        return render(request, "welcome.html", {"author": author})

class PostView(APIView):
    '''
    '''
    def get(self, request, pk):
        post = views.PostView.as_view()(request, pk).data
        form = PostForm()
        comment_form = CommentForm()
        return render(request, "posts-id.html", {"post": post, "post_form": form, "comment_form": comment_form})

class CommentsView(APIView):
    def get(self, request, pk):
        comments = views.CommentAPIView.as_view()(request, pk).data
        post = views.PostView.as_view()(request, pk).data
        form = CommentForm()
        return render(request, "posts-id-comments.html", {"comments": comments,
            "host": request.get_host(), "post": post, "comment_form": form})

class PostsCommentsView(APIView):
    '''
    '''
    def post(self, request, pk):
        views.create_comment(request,pk)
        return redirect("publicPosts")

class AuthorCommentsView(APIView):
    '''
    '''
    def post(self, request, pk):
        views.create_comment(request,pk)
        return redirect("author-detail", pk=pk)

class PostsView(APIView):
    '''
    '''
    #TODO: replace get_public_posts()
    def get(self, request):
        response = views.PostsNodesView.as_view()(request)
        form = CommentForm()
        post_form = PostForm()
        try:
            next_page = response.data["next"]
        except:
            next_page = None
        print next_page
        if (response.status_code == 200):
            return render(request, "posts.html", {"posts":response.data['posts'],
                "comment_form":form, "post_form": post_form, "next":next_page })
        else:
            return HttpResponse(status=response.status_code)

    def post(self, request):
        print "MADE IT TO THE POST"
        views.create_post(request)
        return redirect("public-posts")

class AuthorCreateView(APIView):
    def get(self, request):
        form = AuthorForm()
        return render(request, "create-account.html", {"form": form})

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
        posts = NodeManager.get_author_posts(pk,request.user.id, request.get_host())
        author = views.AuthorDetailView.as_view()(request, pk).data
        return render(request, "author-id-posts.html", {"posts":posts, "host":request.get_host(),
            "author": author })

class AuthorDetailView(APIView):
    '''
    '''
    def get_object(self, user):
        try:
            print "author", Author.objects.get(user=user)
            return Author.objects.get(user=user)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        author = NodeManager.get_author(pk)
        author2 = self.get_object(request.user)
        your_profile = False
        if (str(author2.id) == pk):
            your_profile = True
            posts = NodeManager.get_stream(request.user)
        else:
            posts =  views.AuthorPostsView.as_view()(request, pk).data
        currently_friends = get_author_object(request.user).is_following(author['id'])
        friends = []
        for friend in author["friends"]:
            f = views.AuthorDetailView.as_view()(request, friend["id"]).data
            friends.append(f)
        return render(request, "author-id.html", {"author": author, "friends": friends,
            "host": request.get_host(), "currently_friends":currently_friends,
            "your_profile": your_profile, "posts": posts })

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
        serializer = AuthorSerializer(data=friend_json, context={'request':request})
        if(serializer.is_valid(raise_exception=True)):
            if (not Author.objects.filter(id=serializer.validated_data["id"]).exists()):
                friend = serializer.save()
            else:
                friend = Author.objects.get(id=pk)
            author.add_friend(friend)
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
        friend = NodeManager.get_author(pk)
        serializer = AuthorSerializer(data=friend, context={'request':request})
        if(serializer.is_valid(raise_exception=True)):
            author = get_author_object(request.user)
            if (not Author.objects.filter(id=serializer.validated_data["id"]).exists()):
                friend = serializer.save()
            else:
                friend = Author.objects.get(id=pk)
            print "Adding author here"
            author.add_friend(friend)
            FriendRequest.objects.get(requesting_author_id=pk, author=author).delete()
            return redirect('friend-requests')

class FriendRequestsRemoveView(APIView):

    def post(self, request, pk):
        FriendRequest.objects.get(requesting_author_id=pk, author=Author.objects.get(user=request.user)).delete()
        return redirect('friend-requests')
