from django.contrib.auth.models import User, Group
from rest_framework import serializers
from service.models import Post

class PostSerializer(serializers.ModelSerializer):
    # for optional fields on post: var = CharField(allow_blank=True, required=False)
    class Meta:
        model = Post.Post
        # fields = (
        #     'title',
        #     'source',
        #     'origin',
        #     'description',
        #     'contentType',
        #     'content',
        #     'author',
        #     'comments',
        #     'count',
        #     'size',
        #     'next',
        #     'published',
        #     'id',
        #     'visibility'
        # )
        # for testing, before model is out
        fields = ('author', 'id')
        #ordering = ['-published']
    def create(self, validated_data):
        return Post.Post.objects.create(**validated_data)

    def update(self, post, validated_data):
        post.author = validated_data.get('author', post.author)
        #post.content = validated_data.get('content', post.content)
        post.save()
        return post


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
