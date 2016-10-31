from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^posts/(?P<uuid>[^/]+)/$', views.PostView.as_view(), name='post')
]