from django.contrib import admin
from .models import Home, Address, Comment, Rating

admin.site.register(Home)
admin.site.register(Address)
admin.site.register(Comment)
admin.site.register(Rating)