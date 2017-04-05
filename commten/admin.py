from django.contrib import admin
from .models import Photo, Tickets, User, UserProfile
# Register your models here.
admin.site.register(Tickets)
admin.site.register(Photo)
admin.site.register(User)
admin.site.register(UserProfile)