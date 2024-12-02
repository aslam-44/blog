from django.contrib import admin
from posts.models import *

admin.site.register(Author)
admin.site.register(Category)

class PostsAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date", "short_description")

admin.site.register(Post)

