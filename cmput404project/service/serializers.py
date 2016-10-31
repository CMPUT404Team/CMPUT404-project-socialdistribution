from django.contrib.auth.models import User, Group
from rest_framework import serializers
from service.models import Post

class PostSerializer(serializers.Serializer):
    # for optional fields on post: var = CharField(allow_blank=True, required=False)
    class Meta:
        model = Post
        fields = (
            'title',
            'source',
            'origin',
            'description',
            'contentType',
            'content',
            'author',
            'comments',
            'count',
            'size',
            'next',
            'published',
            'id',
            'visibility'
        )
        ordering = ['-published']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
