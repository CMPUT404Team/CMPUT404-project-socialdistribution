from django.contrib.auth.models import User, Group
from rest_framework import serializers
from service.models import Author

class AuthorSerializer(serializers.Serializer):
    class Meta:
        model = Author
        fields = ('username', 'email', 'groups')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
