from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, frontEndViews
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'))),
    url(r'^doggo/$', frontEndViews.HomeView.as_view(), name='home'),
    url(r'^doggo/welcome/$', frontEndViews.WelcomeView.as_view(), name='welcome'),
    url(r'^posts/$', views.PostsView.as_view(), name='publicPosts'),
    url(r'^doggo/login/$', frontEndViews.LoginView.as_view(), name='login'),
    url(r'^doggo/author/exists/$', frontEndViews.AuthorExistsView.as_view(), name='author_exists'),
    url(r'^posts/(?P<pk>[^/]+)/$', views.PostView.as_view(), name='post'),
    url(r'^author/posts/$', views.VisiblePostsView.as_view(), name='visiblePosts'),
    url(r'^author/add/$', views.create_author, name='create_author'),
    url(r'^posts/add/$', views.create_post, name='createPost'),
    url(r'^author/(?P<pk>[^/]+)/posts/$', views.AuthorPostsView.as_view(), name='authorPosts'),
    url(r'^posts/(?P<pid>[^/]+)/comments', views.CommentAPIView.as_view()),
    url(r'^friendrequest/$', views.FriendRequestView.as_view(), name='friend-request'),
    url(r'^friends/(?P<uuid1>[^/]+)/(?P<uuid2>[^/]+)/$', views.FriendDetailView.as_view(), name='friend-detail'),
    url(r'^friends/(?P<uuid>[^/]+)/$', views.MutualFriendDetailView.as_view(),name='mutual-friend'),
    url(r'^author/(?P<pk>[^/]+)/$', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^doggo/author/awaiting-approval/$', TemplateView.as_view(template_name='awaiting-approval.html'), name='awaiting-approval'),
    url(r'^frontend/posts/$', views.PostsNodesView.as_view(), name='frontend-public-posts'),
    url(r'^frontend/author/posts/$', views.VisiblePostsNodesView.as_view(), name='frontend-visible-posts'),
    url(r'^doggo/posts/$', frontEndViews.PostsView.as_view(), name='public-posts'),
    url(r'^doggo/posts/(?P<pk>[^/]+)/$', frontEndViews.PostView.as_view(), name='post'),
    url(r'^doggo/friends/$', frontEndViews.FriendView.as_view(), name='friend-detail'),
    url(r'^doggo/friendrequests/add/(?P<pk>[^/]+)/$', frontEndViews.FriendRequestsAddView.as_view(), name='add-friend-request'),
    url(r'^doggo/friendrequests/remove/(?P<pk>[^/]+)/$', frontEndViews.FriendRequestsRemoveView.as_view(), name='remove-friend-request'),
    url(r'^doggo/friendrequests/$', frontEndViews.FriendRequestsView.as_view(), name='friend-requests'),
    url(r'^doggo/author/posts/$',frontEndViews.AuthorPostsView.as_view(), name='authorPosts'),
    url(r'^doggo/posts/(?P<pk>[^/]+)/comments', frontEndViews.CommentsView.as_view(), name='comments'),
    url(r'^doggo/posts/posts/(?P<pk>[^/]+)/comments', frontEndViews.PostsCommentsView.as_view(), name='postsComments'),
    url(r'^doggo/author/posts/(?P<pk>[^/]+)/comments', frontEndViews.AuthorCommentsView.as_view(), name='authorComments'),
    url(r'^doggo/author/add/$', frontEndViews.AuthorCreateView.as_view(), name='author-add'),
    url(r'^doggo/author/(?P<pk>[^/]+)/$', frontEndViews.AuthorDetailView.as_view(), name='frontend-author-detail'),
    url(r'^doggo/author/(?P<pk>[^/]+)/befriend/$', frontEndViews.BefriendView.as_view(), name='frontend-befriend'),
    url(r'^doggo/author/(?P<pk>[^/]+)/unfriend/$', frontEndViews.UnfriendView.as_view(), name='frontend-unfriend'),
    url(r'^doggo/author/(?P<pk>[^/]+)/posts/$', frontEndViews.AuthorIdPostsView.as_view(), name='authorIdPosts'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
