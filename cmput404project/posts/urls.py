from django.conf.urls import url

from . import views


urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^doggo/posts/$', views.PostsView.as_view(), name='publicPosts'),
            url(r'^doggo/posts/(?P<pk>[^/]+)/$', views.PostView.as_view(), name='post'),
            url(r'^doggo/friends/$', views.FriendView.as_view(), name='friend-detail'),
            url(r'^doggo/author/posts/$', views.AuthorPostsView.as_view(), name='authorPosts'),
            url(r'^posts/(?P<pk>[^/]+)/comments', views.CommentView.as_view())
            ]
