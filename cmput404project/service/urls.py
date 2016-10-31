from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^posts/(?P<uuid>[^/]+)/$', views.PostDetailView.as_view(), name='post')
]