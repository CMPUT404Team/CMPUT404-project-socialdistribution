from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models.Author import Author
import uuid

class FriendSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField()
    class Meta:
        model = Author
        fields = ('url', 'id', 'displayName', 'host')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    friends = FriendSerializer(required=False, many=True)
    class Meta:
        model = Author
        fields = ('url', 'id', 'displayName', 'host', 'friends')

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
