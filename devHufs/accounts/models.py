# from django.db import models
# from django.contrib.auth.models import AbstractUser, Group, Permission
# from allauth.socialaccount.models import SocialApp
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from dotenv import load_dotenv
# #from .models import GoogleAccount
# import os
# load_dotenv()



# # 사용자 정보
# class User(AbstractUser):
#     name = models.CharField(max_length=100, null=False)
#     profile_img = models.ImageField(null=True)
#     student_num = models.IntegerField(null=True)
#     stack = models.CharField(max_length=100, null=False)
#     groups = models.ManyToManyField(Group, related_name='user_groups')
#     user_permissions = models.ManyToManyField(Permission, related_name='user_permissions')


# # 구글 소셜 계정 모델
# class GoogleAccount(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='google_account')
#     email = models.EmailField(unique=True)


# class GoogleSocialApp(SocialApp):
#     class Meta:
#         proxy = True

#     def save(self, *args, **kwargs):
#         self.provider = 'google'
#         self.name = 'Google'
#         self.client_id = os.getenv('SOCIAL_AUTH_GOOGLE_CLIENT_ID')
#         self.secret_key = os.getenv('YOUR_GOOGLE_SECRET_KEY')
#         self.sites.clear()
#         self.sites.add(1)
#         super().save(*args, **kwargs)

# # User 모델이 저장될 때 GoogleAccount 모델도 자동으로 생성되도록 설정
# @receiver(post_save, sender=get_user_model())
# def create_google_account(sender, instance, created, **kwargs):
#     if created:
#         user_instance = get_user_model().objects.get(pk=instance.pk)
#         GoogleAccount.objects.create(user=user_instance)


# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from allauth.socialaccount.models import SocialAccount


from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.socialaccount.models import SocialAccount
# Create your models here.


class Blog(models.Model):
    text = models.TextField()