from django.contrib import admin
from models.Post import Post
from models.Category import Category
from models.Comment import Comment
from models.Author import Author
from models.Node import Node
from models.NodeManager import NodeManager
from models.FriendRequest import FriendRequest

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Node)
admin.site.register(FriendRequest)
