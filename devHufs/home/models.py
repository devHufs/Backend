from django.db import models
from accounts.models import *

# Create your models here.

class Content(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(default="")
    attached = models.FileField(upload_to='uploads/')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User, related_name='like_contents')
    scrap_users = models.ManyToManyField(User, related_name='scrap_contents')
    like_cnt = models.IntegerField(default=0)
    comment_cnt = models.IntegerField(default=0)
    scrap_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content_num = models.ForeignKey(Content, on_delete=models.CASCADE, null=True)
    body = models.TextField(default="")
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)