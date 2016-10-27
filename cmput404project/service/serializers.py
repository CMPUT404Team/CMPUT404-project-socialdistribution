from django.contrib.auth.models import User, Group
from rest_framework import serializers
from service.models import Author

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('url', 'username', 'email', 'groups', 'iden')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    iden = serializers.UUIDField(source='author.iden')
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups','iden')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
