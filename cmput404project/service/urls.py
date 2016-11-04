from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^friends/(?P<uuid1>[^/]+)/(?P<uuid2>[^/]+)$', views.FriendDetailView.as_view())
	url(r'^friends/(?P<uuid>[^/]+)/', views.MutualFriendDetailView.as_view()),
        url(r'^friendrequest$', views.FriendRequestView.as_view(), name='friend-request'),
        url(r'^author/add/$', views.AuthorCreate.as_view(), name='author-add'),
	url(r'^author/(?P<pk>[^/]+)/$', views.AuthorDetailView.as_view(), name='author-detail')
]
