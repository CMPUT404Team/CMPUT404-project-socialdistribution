from django.conf.urls import url

from . import views


urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^frontend/posts/$', views.PostsView.as_view(), name='publicPosts'),
            url(r'^frontend/friends/$', views.FriendView.as_view(), name='friend-detail'),
            url(r'^frontend/author/posts/$', views.AuthorPostsView.as_view(), name='authorPosts')
            ]
