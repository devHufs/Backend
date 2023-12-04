from rest_framework import serializers
from .models import Content, Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['content_num']

class ContentSerilaizer(serializers.ModelSerializer):
    # comments = serializers.SerializerMethodField() #댓글 불러옴
    # likes = serializers.SerializerMethodField()
    # scraps = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'title', 'date', 'body', 'attached', 'like_cnt', 'comment_cnt', 'scrap_cnt'] 
        read_only_fields = ['user', 'like_cnt', 'comment_cnt', 'scrap_cnt']
        #like_users, scrap_users, users, comments 필드 필요시 추가


class CommentListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['comments']
        
    def get_comments(self, obj):
        comments = Comment.objects.filter(content_num=obj)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data
    

# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Content
#         fields = ['like_users', 'like_cnt']


# class ScrapSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Content
#         fields = ['scrap_users', 'scrap_cnt']
