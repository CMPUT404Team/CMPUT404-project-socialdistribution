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
    
class FriendRequestSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super(self.__class__,self).__init__(*args, **kwargs)
        self.fields['author'] = FriendSerializer(required=False, context=self.context)
        self.fields['friend'] = FriendSerializer(required=False, context=self.context)

