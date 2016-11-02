from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^posts/(?P<id>[^/]+)/comments', views.CommentAPIView.as_view()),
	url(r'^author/(?P<uuid>[^/]+)/$', views.AuthorDetailView.as_view(), name='author')
]
