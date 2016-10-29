from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.encoding import python_2_unicode_compatible
import uuid

@python_2_unicode_compatible
class Author(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    iden = models.UUIDField()
    host = models.CharField(default='')
    image = models.CharField(default='')
    posts=[]
    friends=[]
    
    def getRandomImageUrl(self):
        return ''

    def __str__(self):
        return self.user.username 
    '''
    def getEmail(self):
        return self.email
    def changePassword(self,newPassword):
        __password=newPassword;
    def getFriends(self):
        return self.friends;
    def getFollowing(self):
        return self.following;
    def getPosts(self):
        return self.posts;
    def friendRequest(self, Auth):
        if Auth.iden in followers:
            #switch Auth to friends
            followers.remove(Auth)
            friends.append(Auth)
            #removing self from following
            Auth.getFollowing().remove(self)
            Auth.getFriends().append(self)
        else:
            following.append(Auth)
            Auth.followers.append(self)

    def deleteFriend(self,Auth):
        friends.remove(Auth)
        followers.append(Auth)
        Auth.getFriends().remove(self)
        Auth.getFollowing().append(self)

    def getProfilePic():
        #get pic passed from sign-up
        pass
    '''
