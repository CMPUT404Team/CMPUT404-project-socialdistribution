from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^posts/$', views.PostsView.as_view(), name='publicPosts'),
    url(r'^posts/(?P<pk>[^/]+)/$', views.PostView.as_view(), name='post'),
    url(r'^author/posts/$', views.VisiblePostsView.as_view(), name='visiblePosts'),
    url(r'^author/(?P<uuid>[^/]+)/posts/$', views.AuthorPostsView.as_view(), name='authorPosts'),
    url(r'^posts/(?P<pid>[^/]+)/comments', views.CommentAPIView.as_view()),
    url(r'^author/add/$', views.AuthorCreate.as_view(), name='author-add'),
    url(r'^friendrequest/$', views.FriendRequestView.as_view(), name='friend-request'),
    url(r'^friends/(?P<uuid1>[^/]+)/(?P<uuid2>[^/]+)$', views.FriendDetailView.as_view(), name='friend-detail'),
    url(r'^friends/(?P<uuid>[^/]+)/', views.MutualFriendDetailView.as_view(),name='mutual-friend'),
    url(r'^author/(?P<pk>[^/]+)/$', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^author/awaiting-approval$', TemplateView.as_view(template_name='awaiting-approval.html'), name='awaiting-approval')
]

urlpatterns = format_suffix_patterns(urlpatterns)

