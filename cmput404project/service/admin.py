from django.contrib import admin
from models.Comment import Comment
from models.Author import Author

# Register your models here.

admin.site.register(Comment)
admin.site.register(Author)
