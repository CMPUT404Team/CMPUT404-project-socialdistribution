from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^author/(?P<uuid>[^/]+)/$', views.AuthorDetailView.as_view(), name='author')
]
