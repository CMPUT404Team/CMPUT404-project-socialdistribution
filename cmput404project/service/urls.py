from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^posts/$', views.PostsView.as_view(), name='publicPosts'),
    url(r'^posts/(?P<pk>[^/]+)/$', views.PostView.as_view(), name='post'),
    url(r'^author/posts/$', views.VisiblePostsView.as_view(), name='visiblePosts'),
    url(r'^author/(?P<uuid>[^/]+)/posts/$', views.AuthorPostsView.as_view(), name='authorPosts'),
    url(r'^posts/(?P<pid>[^/]+)/comments', views.CommentAPIView.as_view()),
    url(r'^author/add/$', views.AuthorCreate.as_view(), name='author-add'),
    url(r'^friendrequest/$', views.FriendRequestView.as_view(), name='friend-request'),
	url(r'^friends/(?P<uuid>[^/]+)/', views.MutualFriendDetailView.as_view()),
	url(r'^friends/(?P<uuid1>[^/]+)/(?P<uuid2>[^/]+)$', views.FriendDetailView.as_view()),
	url(r'^author/(?P<pk>[^/]+)/$', views.AuthorDetailView.as_view(), name='author-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
