from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import TemplateHTMLRenderer
import urllib2, base64, json, os
from rest_framework.views import APIView
from django.template.response import TemplateResponse
from django.conf import settings
from service.models.Author import Author

def index(index):
    return redirect("author-add")

def get_json_from_api(url):
    req = urllib2.Request(url)
    base64string = base64.b64encode('%s:%s' % (getattr(settings, 'USERNAME'), os.environ.get('FRONTEND_PASSWORD')))
    req.add_header("Authorization", "Basic %s" % base64string)
    serialized_data = urllib2.urlopen(req).read()
    print serialized_data
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
        print url
        comments = get_json_from_api(url)
        print comments
        return render(request, "posts-id-comments.html", {"comments": comments})

class PostsView(APIView):
    '''
    '''
    def get(self, request):
        url = getattr(settings, 'CURRENT_HOST') + 'frontend/posts/'
        posts = get_json_from_api(url)
        return render(request, "posts.html", {"posts":posts['posts']})

class AuthorPostsView(APIView):
    '''
    '''
    def get(self, request):
        url = getattr(settings, 'CURRENT_HOST') + 'frontend/author/posts/'
        posts = get_json_from_api(url)
        return render(request, "author-posts.html", {"posts":posts['posts']})

class FriendView(APIView):
    def get(self, request):
        author = Author.objects.filter(user_id = request.user.id
        url = getattr(settings, 'CURRENT_HOST') + 'friends/' + str(author.id) + '/'
        # url = "127.0.0.1:8000/friends/" + str(author.id) + '/'
        friends = get_json_from_api(url)
        return render(request, "friends.html", {"friends":friends})
