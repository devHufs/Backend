from django.db import models
from accounts.models import *


# Create your models here.

class Content(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(default="")
    date = models.DateTimeField(auto_now_add=True)
    #둘 중 하나는 필수입력으로 들어가야 함
    attached = models.FileField(upload_to='uploads/', null=True)
    link = models.URLField(max_length=200, default = " ", null=True)
    # stack = ArrayField(models.CharField(max_length=10), blank=True, null=True)
        # 어떻게 전달될지 몰라서 일단 UserProfile.stack이랑 동일하게 해놓음
    job = models.CharField(max_length=100, blank=True, default=" ", null=True) 
    
    # User 모델 연결 후 주석 풀기
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(UserProfile, null=True, related_name='like_contents')
    scrap_users = models.ManyToManyField(UserProfile, null=True, related_name='scrap_contents')

    like_cnt = models.IntegerField(default=0)
    comment_cnt = models.IntegerField(default=0)
    scrap_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content_num = models.ForeignKey(Content, on_delete=models.CASCADE, null=True)
    body = models.TextField(default="")
    date = models.DateTimeField(auto_now_add=True)

    comment_user = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)