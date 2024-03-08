from django.contrib import admin
from .models import UserProfile
from accounts.models import Album

admin.site.register(UserProfile)
admin.site.register(Album)
