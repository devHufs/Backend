# from django.contrib import admin
# from allauth.socialaccount.models import SocialApp
# from .models import User, GoogleAccount, GoogleSocialApp

# admin.site.register(User)

# @admin.register(GoogleSocialApp)
# class GoogleSocialAppAdmin(admin.ModelAdmin):
#     list_display = ('name', 'client_id', 'sites_display')

#     def sites_display(self, obj):
#         return ", ".join([site.name for site in obj.sites.all()])
#     sites_display.short_description = 'Sites'


from django.contrib import admin
from .models import GoogleLogin, User

admin.site.register(GoogleLogin)
admin.site.register(User)