from django.contrib import admin
from .models import GoogleLogin, User

admin.site.register(GoogleLogin)
admin.site.register(User)