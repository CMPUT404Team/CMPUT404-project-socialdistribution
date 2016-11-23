from django.conf.urls import url

from . import views


urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^dogo/posts/$', views.PostsView.as_view(), name='publicPosts'),
            url(r'^dogo/friends/$', views.FriendView.as_view(), name='friend-detail'),
            url(r'^dogo/author/posts/$', views.AuthorPostsView.as_view(), name='authorPosts')
            ]
