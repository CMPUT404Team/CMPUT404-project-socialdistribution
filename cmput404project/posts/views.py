from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import TemplateHTMLRenderer
import urllib2, base64, json, os
from rest_framework.views import APIView
from django.template.response import TemplateResponse
from django.conf import settings

def index(index):
    return redirect("author-add")

def get_json_from_api(self, url):
    req = urllib2.Request(url)
    base64string = base64.b64encode('%s:%s' % (getattr(settings, 'USERNAME'), os.environ.get('FRONTEND_PASSWORD')))
    req.add_header("Authorization", "Basic %s" % base64string)
    serialized_data = urllib2.urlopen(req).read()
    return json.loads(serialized_data)

class PostView(APIView):
    '''
    '''
    def get(self, request, pk):
        url = getattr(settings, 'CURRENT_HOST') + '/posts/' + str(pk)
        post = get_data_from_api(url)
        return render(request, "posts-id.html", {"post":post})

class CommentView(APIView):
    '''
    '''
    def get(self, request, pk):
        url = getattr(settings, 'CURRENT_HOST') + '/posts/' + str(pk) + '/comments/'
        post = get_data_from_api(url)
        return render(request, "posts-id-comments.html", {"post":post})

class PostsView(APIView):
    '''
    '''
    def get(self, request):
        url = getattr(settings, 'CURRENT_HOST') + 'frontend/posts/'
        posts = get_data_from_api(url)
        return render(request, "posts.html", {"posts":posts['posts']})

class AuthorPostsView(APIView):
    '''
    '''
    def get(self, request):
        url = getattr(settings, 'CURRENT_HOST') + 'frontend/author/posts/'
        posts = get_data_from_api(url)
        return render(request, "author-posts.html", {"posts":posts['posts']})

class FriendView(APIView):
    def get(self, request):
        username = request.user.username
        url = getattr(settings, 'CURRENT_HOST') + 'friends/' + str(username)
        friends = get_data_from_api(url)
        return render(request, "friends.html", {"friends":friends})
