from django.conf.urls import url

from . import views


urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^frontend/posts/$', views.PostsView.as_view(), name='publicPosts')
            ]
