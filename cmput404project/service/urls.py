from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^posts/$', views.PostsView.as_view(), name='posts'),
    url(r'^posts/(?P<uuid>[^/]+)/$', views.PostView.as_view(), name='post')
]

urlpatterns = format_suffix_patterns(urlpatterns)