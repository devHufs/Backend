from rest_framework import serializers
from .models import *
from accounts.models import *
from accounts.serializers import *

class CommentSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'date', 'comment_user', 'user_profile', 'body']
        read_only_fields = ['content_num']

    def get_user_profile(self, obj):
        user_profile = obj.comment_user
        serializer = UserSerializer(user_profile)
        return serializer.data


class ContentSerializer(serializers.ModelSerializer):
    # comments = serializers.SerializerMethodField()
    user_profile = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'title', 'date', 'user', 'user_profile', 'body', 'job', 'link', 'attached', 'like_cnt', 'comment_cnt', 'scrap_cnt']
        read_only_fields = ['like_cnt', 'comment_cnt', 'scrap_cnt']
    
    def get_user_profile(self, obj):
        user_profile = obj.user
        serializer = UserSerializer(user_profile)
        return serializer.data
    

class ContentListSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'title', 'date', 'user_profile', 'like_cnt', 'comment_cnt', 'scrap_cnt']

    def get_user_profile(self, obj):
        user_profile = obj.user
        serializer = UserSerializer(user_profile)
        return serializer.data


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
# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Content
#         fields = ['like_users', 'like_cnt']

# class ScrapSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Content
#         fields = ['scrap_users', 'scrap_cnt']

class LikesWithUserSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['contents']

    def get_contents(self, obj):
        liked_contents = obj.like_contents.all()
        serializer = ContentListSerializer(liked_contents, many=True)
        return serializer.data



class ScrapsWithUserSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['contents']

    def get_contents(self, obj):
        scrapped_contents = obj.scrap_contents.all()
        serializer = ContentListSerializer(scrapped_contents, many=True)
        return serializer.data
