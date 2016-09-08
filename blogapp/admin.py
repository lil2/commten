from django.contrib import admin
from .models import Photo, Post, User
# Register your models here.
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(User)
