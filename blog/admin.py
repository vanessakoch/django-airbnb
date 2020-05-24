from django.contrib import admin
from .models import Post, Comment, PostLike, PostDislike

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostLike)
admin.site.register(PostDislike)
