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

def get_json_from_api(url):
    req = urllib2.Request(url)
    password = os.environ.get('FRONTEND_PASSWORD')
    if (password == ''):
        print
        print "You didn't specify FRONTEND_PASSWORD as an environment variable"
        print
        raise Exception("You didn't specify FRONTEND_PASSWORD as an environment variable")
    base64string = base64.b64encode('%s:%s' % (getattr(settings, 'USERNAME'), os.environ.get('FRONTEND_PASSWORD')))
    req.add_header("Authorization", "Basic %s" % base64string)
    serialized_data = urllib2.urlopen(req).read()
    return json.loads(serialized_data)

class PostView(APIView):
    '''
    '''
    def get(self, request, pk):
        url = getattr(settings, 'CURRENT_HOST') + '/posts/' + str(pk)
        post = get_json_from_api(url)
        return render(request, "posts-id.html", {"post":post})

class CommentsView(APIView):
    '''
    '''
    def get(self, request, pk):
        url = getattr(settings, 'CURRENT_HOST') + '/posts/' + str(pk) + '/comments/'
        post_url = getattr(settings, 'CURRENT_HOST') + '/posts/' + str(pk)
        comments = get_json_from_api(url)
        post = get_json_from_api(post_url)
        return render(request, "posts-id-comments.html", {"comments": comments, "host": getattr(settings, 'CURRENT_HOST'), "post": post})

class PostsView(APIView):
    '''
    '''
    def get(self, request):
        response = views.PostsView.as_view()(request) 
        if (response.status_code == 200):
            return render(request, "posts.html", {"posts":response.data['posts'], "host": getattr(settings, 'CURRENT_HOST')})
        else:
            return HttpResponse(status=response.status_code)

class AuthorPostsView(APIView):
    '''
    '''
    def get(self, request):
        url = getattr(settings, 'CURRENT_HOST') + '/frontend/author/posts/'
        posts = get_json_from_api(url)
        return render(request, "author-posts.html", {"posts":posts['posts']})

class AuthorIdPostsView(APIView):
    '''
    '''
    def get(self, request, pk):
        url = getattr(settings, 'CURRENT_HOST') + '/author/'+ str(pk)+'/posts/'
        author_url = getattr(settings, 'CURRENT_HOST') + '/author/'+ str(pk)
        posts = get_json_from_api(url)
        author = get_json_from_api(author_url)
        return render(request, "author-id-posts.html", {"posts":posts, "host": getattr(settings, 'CURRENT_HOST'), "author": author })

class FriendView(APIView):
    def get(self, request):
        author = Author.objects.filter(user_id = request.user.id)[0]
        url = getattr(settings, 'CURRENT_HOST') + '/friends/' + str(author.id) + '/'
        # url = "127.0.0.1:8000/friends/" + str(author.id) + '/'
        friends = get_json_from_api(url)
        return render(request, "friends.html", {"friends":friends})
