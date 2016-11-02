from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^1/comments', views.CommentAPIView.as_view()),
	url(r'^author/(?P<uuid>[^/]+)/$', views.AuthorDetailView.as_view(), name='author')
]
