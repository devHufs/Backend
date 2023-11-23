from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount
# Create your models here.


class Blog(models.Model):
    text = models.TextField()