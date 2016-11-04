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
    friends = FriendSerializer()
    class Meta:
        model = Author
        fields = ('url', 'id', 'displayName', 'host', 'friends')

class FriendIDSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super(self.__class__,self).__init__(*args, **kwargs)
	self.fields['id'] = serializers.UUIDField()

class FriendListSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=50)
    # authors = FriendIDSerializer()
    def __init__(self, *args, **kwargs):
        super(self.__class__,self).__init__(*args, **kwargs)
        self.fields['author'] = serializers.UUIDField()
	self.fields['authors'] = serializers.Serialize() 
	
class FriendRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=50)
    author = FriendSerializer()
    friend = FriendSerializer()
