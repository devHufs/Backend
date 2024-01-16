from django.db import models
from django.contrib.postgres.fields import ArrayField
#import uuid

class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100, unique=True, null=False)
    name = models.CharField(max_length=100)
    pic = models.ImageField(blank=True, null=True)
    student_num = models.IntegerField(unique=True, blank=True, null=True, default=0)
    job = models.CharField(max_length=100, blank=True, null=True, default="")
    stack = ArrayField(models.CharField(max_length=50), blank=True, default=list)
