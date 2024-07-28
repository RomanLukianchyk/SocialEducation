from django.contrib import admin
from .models import Post, Image, Tag, PostTag

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(PostTag)
