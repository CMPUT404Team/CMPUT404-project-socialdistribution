from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^author/add/$', views.AuthorCreate.as_view(), name='author-add'),
	url(r'^author/(?P<uuid>[^/]+)/$', views.AuthorDetailView.as_view(), name='author-detail'),
]
