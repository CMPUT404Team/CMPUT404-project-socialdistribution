from django.contrib.auth.models import User, Group
from rest_framework import serializers
from service.models import Comment, Author, Post
from django.db import models
from models.Author import Author
from models.Comment import Comment
import uuid

class FriendSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'id', 'displayName', 'host')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    friends = FriendSerializer(required=False, many=True)
    class Meta:
        model = Author
        fields = ('url', 'id', 'displayName', 'host', 'friends')

class PostSerializer(serializers.ModelSerializer):
    # for optional fields on post: var = CharField(allow_blank=True, required=False)
    #author = AuthorSerializer(context=this.context, required=True)
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

class CommentSerializer(serializers.Serializer):
    author = AuthorSerializer()
    pubDate = serializers.DateTimeField()
    comment= serializers.CharField(max_length=200)
    guid = serializers.UUIDField()

    def create(self, validated_data):
        print (validated_data)
        #validated_data[]
        return Comment.create_comment(**validated_data)

    def update(self, instance, validated_data):
        print "update"
        # probs going to have to call AuthorSerializer to deserialize
        #instance.author = validated_data.get('author', instance.email)
        #instance.pubDate = validated_data.get('pubDate', instance.pubDate)
        instance.comment = validated_data.get('comment', instance.comment)
        #not sure about guid
        instance.guid = validated_data.get('guid', instance.guid)
        instance.save()
        return instance
