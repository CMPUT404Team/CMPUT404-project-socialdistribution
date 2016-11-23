from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import TemplateHTMLRenderer
import urllib2, base64
import json
from rest_framework.views import APIView
from django.template.response import TemplateResponse
import os

def index(index):
    return redirect("author-add")

class PostsView(APIView):
    '''
    '''
    username = 'dogordie'
    # username = 'admin'
    # password='superuser'
    password = os.environ.get('FRONTEND_PASSWORD')
    # host = 'http://localhost:8000/'
    host = 'http://winter-resonance.herokuapp.com/'
    def get(self, request):
        url = self.host + 'frontend/posts/'
        req = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        req.add_header("Authorization", "Basic %s" % base64string)
        serialized_data = urllib2.urlopen(req).read()
        posts = json.loads(serialized_data)
        return render(request, "posts.html", {"posts":posts['posts']})

class AuthorPostsView(APIView):
    '''
    '''
    username = 'dogordie'
    # username = 'admin'
    # password='superuser'
    password = os.environ.get('FRONTEND_PASSWORD')
    # host = 'http://localhost:8000/'
    host = 'http://winter-resonance.herokuapp.com/'
    def get(self, request):
        url = self.host + 'frontend/author/posts/'
        req = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (self.username, self.password))
        req.add_header("Authorization", "Basic %s" % base64string)
        serialized_data = urllib2.urlopen(req).read()
        posts = json.loads(serialized_data)
        return render(request, "author-posts.html", {"posts":posts['posts']})

class FriendView(APIView):
    username = 'dogordie'
    password = os.environ.get('FRONTEND_PASSWORD')
    username = 'admin'
    password = 'superuser'
    host = 'http://winter-resonance.herokuapp.com/'
    def get(self, request):
        username = request.user.username
        
        url = self.host + 'friends/' + str(username)
        req = urllib2.Request(url)
        base64string = base64.b64encode('%s:%s' % (username, self.password))
        req.add_header("Authorization", "Basic %s" % base64string)
        serialized_data = urllib2.urlopen(req).read()
        friends = json.loads(serialized_data)
        return render(request, "friends.html", {"friends":friends})
