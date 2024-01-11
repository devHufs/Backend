from django.db import models
from django.contrib.postgres.fields import ArrayField
#import uuid

class UserProfile(models.Model):
    #user_id = models.BigIntegerField(unique=True, null=False)
    email = models.EmailField(max_length=100, unique=True, null=False)
    name = models.CharField(max_length=100)
    pic = models.ImageField(blank=True, null=True)
    student_num = models.IntegerField(unique=True, blank=True, null=True, default=0)
    job = models.CharField(max_length=100, blank=True, null=True, default="")
    #stack = ArrayField(models.CharField(max_length=10), blank=True, null=True)
    # 어떤 db 쓰느냐에 따라 달라짐

    # def save(self, *args, **kwargs):
    #     if not self.user_id:
    #         self.user_id = str(uuid.uuid4())[:8]  # 8자리의 UUID 사용 (적절한 길이로 조절 가능)
    #     super(UserProfile, self).save(*args, **kwargs)