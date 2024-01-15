from rest_framework import serializers
from .models import *
from accounts.models import *

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['content_num']

class ContentSerializer(serializers.ModelSerializer):
    # comments = serializers.SerializerMethodField() #댓글 불러옴

    class Meta:
        model = Content
        #User모델 연결 후 'user'추가 필요
        fields = ['id', 'title', 'date', 'user', 'body', 'job', 'link', 'attached', 'like_cnt', 'comment_cnt', 'scrap_cnt']
        # fields = ['id', 'title', 'date', 'body', 'attached', 'like_cnt', 'comment_cnt', 'scrap_cnt']  
        read_only_fields = ['like_cnt', 'comment_cnt', 'scrap_cnt']
        #like_users, scrap_users, comments 필드 필요시 추가


class CommentListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['comments']
        
    def get_comments(self, obj):
        comments = Comment.objects.filter(content_num=obj)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data
    

#User모델 연결 후 주석풀기
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['like_users', 'like_cnt']

class ScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['scrap_users', 'scrap_cnt']

class LikesWithUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['like_contents']

class ScrapsWithUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['scrap_contents']
