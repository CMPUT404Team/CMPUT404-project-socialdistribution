from django.contrib import admin
from models.Post import Post
from models.Category import Category
from models.Comment import Comment
from models.Author import Author

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Author)
