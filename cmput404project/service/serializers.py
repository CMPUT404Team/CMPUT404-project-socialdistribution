from django.contrib.auth.models import User, Group
from rest_framework import serializers
import uuid

class FriendSerializer(serializers.Serializer):
    displayName = serializers.CharField()
    id = serializers.UUIDField()
    host = serializers.CharField()	 

class AuthorSerializer(serializers.Serializer):
    displayName = serializers.CharField()
    id = serializers.UUIDField()
    host = serializers.CharField()
    friends = FriendSerializer(required=False, many=True)
      
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
