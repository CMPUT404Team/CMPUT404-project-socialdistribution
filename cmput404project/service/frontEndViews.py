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
from . import views
from django.views.generic.edit import FormView
from rest_framework.response import Response
from AuthorForm import AuthorForm
from AuthorExistsForm import AuthorExistsForm
from LoginForm import LoginForm
from serializers import AuthorSerializer
from models.NodeManager import NodeManager
import ast
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

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
    def get(self, request):
        print request.user.is_authenticated
        if not request.user.is_authenticated:
            form = AuthorExistsForm()
            return render(request, 'home.html', {'form': form})
        else:
            form = AuthorExistsForm()
            return render(request, 'home.html', {'form': form})

class AuthorExistsView(APIView):
    def get(self, request):
        form = LoginForm()
        return redirect("login")

    def post(self, request):
        self.username = request.POST['displayName']
        user_exists = get_author_exists(self.username)
        if user_exists:
            return redirect("login")
        else:
            return redirect("create_author")

class LoginView(APIView):
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
    #TODO: replace get_public_posts()
    def get(self, request):
        response = views.PostsView.as_view()(request)
        if (response.status_code == 200):
            return render(request, "posts.html", {"posts":response.data['posts'], })
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
        author2 = self.get_object(request.user)
        author = views.AuthorDetailView.as_view()(request, pk).data
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

    def get_friend_json(self, raw_friend_data):
        return ast.literal_eval(raw_friend_data)

    def post(self, request):
        try:
            author = get_author_object(request.user)
            author_json = AuthorSerializer(author, context={'request':request}).data
            request_dict = dict(request.data.iterlists())
            currently_friends = request_dict.get("currently_friends")[0]
            friend_json = self.get_friend_json(request_dict.get("friend")[0])
            if (currently_friends == str(True)):
                #You are unfriending them
                author.remove_friend(Author.objects.get(id=friend_json['id']))
            else:
                #You are befriending them
                status_code = NodeManager.befriend(author_json, friend_json)
            request.method = "get"
            return AuthorDetailView.as_view()(request, friend_json['id'])
        except:
            return Response(status=400)
