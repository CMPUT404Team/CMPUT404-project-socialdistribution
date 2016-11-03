from django.contrib.auth.models import User, Group
from rest_framework import serializers
from service.models import Post, Author
from django.db import models


class PostSerializer(serializers.ModelSerializer):
    # for optional fields on post: var = CharField(allow_blank=True, required=False)
    author = models.ForeignKey(Author.Author)
    class Meta:
        model = Post.Post
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
    def create(self, validated_data):
        return Post.Post.objects.create(**validated_data)

    def update(self, post, validated_data):
        post.title = validated_data.get('title', post.title)
        post.source = validated_data.get('source', post.source)
        post.origin = validated_data.get('origin', post.origin)
        post.description = validated_data.get('description', post.description)
        post.contentType = validated_data.get('contentType', post.contentType)
        post.content = validated_data.get('content', post.content)
        post.author = validated_data.get('author', post.author)
        post.comments = validated_data.get('comments', post.comments)
        post.count = validated_data.get('count', post.count)
        post.size = validated_data.get('size', post.size)
        post.next = validated_data.get('next', post.next)
        post.published = validated_data.get('published', post.published)
        post.id = validated_data.get('id', post.id)
        post.visibility = validated_data.get('visibility', post.visibility)
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
