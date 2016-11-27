from django.contrib.auth.models import User, Group
from rest_framework import serializers
from service.models import Comment, Author, Post
from models.Author import Author
from models.Post import Post
from django.db import models
from models.Comment import Comment
import uuid

class FriendSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Author
        fields = ('url', 'id', 'displayName', 'host')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField()
    friends = FriendSerializer(required=False, many=True)
    class Meta:
        model = Author
        fields = ('url', 'id', 'displayName', 'host', 'friends')

class CommentSerializer(serializers.Serializer):
    author = AuthorSerializer()
    pubDate = serializers.DateTimeField()
    comment= serializers.CharField(max_length=200)
    guid = serializers.UUIDField()

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        #author_id = post=validated_data['author']['id']
        #author = Author.objects.get(id = author_id)
        #comment.save(post=validated_data['post']['id'])
        return comment
        #author=AuthorSerializer(data=validated_data["author"])
        #return Comment.create_comment(validated_data['comment'],validated_data["author"],post)

    def update(self, instance, validated_data):
        # probs going to have to call AuthorSerializer to deserialize
        #instance.author = validated_data.get('author', instance.email)
        #instance.pubDate = validated_data.get('pubDate', instance.pubDate)
        instance.comment = validated_data.get('comment', instance.comment)
        #not sure about guid
        instance.guid = validated_data.get('guid', instance.guid)
        instance.save()
        return instance

class PostSerializerGet(serializers.ModelSerializer):
    # for optional fields on post: var = CharField(allow_blank=True, required=False)
    id = serializers.UUIDField()
    author = FriendSerializer()
    comments = CommentSerializer(required=False, many=True)
    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'content',
        'contentType','description', 'author','count','size',
        'next','comments','published','id','visibility')

    def create(self, validated_data):
        author_id = validated_data.pop('author')['id']
        author = Author.objects.get(id=author_id)
        return Post.objects.create(author=author,**validated_data)

    def update(self, post, validated_data):
        author_id = validated_data.pop('author')['id']
        author = Author.objects.get(id=author_id)
        post.title = validated_data.pop('title')
        post.source = validated_data.pop('source', post.source)
        post.origin = validated_data.get('origin', post.origin)
        post.description = validated_data.get('description', post.description)
        post.contentType = validated_data.get('contentType', post.contentType)
        post.content = validated_data.get('content', post.content)
        post.count = validated_data.get('count', post.count)
        post.size = validated_data.get('size', post.size)
        post.next = validated_data.get('next', post.next)
        post.published = validated_data.get('published', post.published)
        post.id = validated_data.get('id', post.id)
        post.visibility = validated_data.get('visibility', post.visibility)
        post.save()
        return post

class PostSerializerPutPost(serializers.ModelSerializer):
    # for optional fields on post: var = CharField(allow_blank=True, required=False)
    id = serializers.UUIDField()
    author = FriendSerializer()

    class Meta:
        model = Post
        fields = ('title', 'source', 'origin', 'content',
        'contentType','description', 'author','count','size',
        'next', 'published','id','visibility')

    def create(self, validated_data):
        author_id = validated_data.pop('author')['id']
        author = Author.objects.get(id=author_id)
        return Post.objects.create(author=author, **validated_data)

    def update(self, post, validated_data):
        author_id = validated_data.pop('author')['id']
        author = Author.objects.get(id=author_id)
        post.title = validated_data.pop('title')
        post.source = validated_data.pop('source', post.source)
        post.origin = validated_data.get('origin', post.origin)
        post.description = validated_data.get('description', post.description)
        post.contentType = validated_data.get('contentType', post.contentType)
        post.content = validated_data.get('content', post.content)
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

class CommentSerializer(serializers.ModelSerializer):
    author=AuthorSerializer()
    guid=serializers.UUIDField()
    class Meta:
        model=Comment
        fields=('author','pubDate','comment','guid')

class CommentSerializerPost(serializers.Serializer):
    author = AuthorSerializer()
    comment= serializers.CharField(max_length=200)

    class Meta:
        model=Comment
        fields=('author','pubDate','comment','guid')

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

class FriendListSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=50)
    author = serializers.UUIDField()
    authors = serializers.ListField(
	    child = serializers.UUIDField()
    )

class FriendRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=50)
    author = FriendSerializer()
    friend = FriendSerializer()
