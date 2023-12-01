from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialApp

class GoogleLogin(models.Model):
    platform = models.CharField(max_length=20, default = 0)

    class Meta:
        db_table = 'google_login'

class User(models.Model):
    social = models.ForeignKey(GoogleLogin, on_delete=models.CASCADE, max_length=20, blank=True, default=1)
    social_login_id = models.CharField(max_length=50, blank=True)


