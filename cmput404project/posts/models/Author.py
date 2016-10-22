from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import uuid

@python_2_unicode_compatible
class Author(models.Model):
    iden=uuid.uuid4()
    username=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    __password=models.CharField(max_length=200)
    image="path"
    posts=[]
    friends=[]
    followers=[]
    following=[]
    host=""
    
    def __str__(self):
        return self.username
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

    def getFeed():
        
