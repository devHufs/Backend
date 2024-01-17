from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view

import datetime
from .serializers import *
from .models import *
from accounts.models import *

from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q

# Create your views here.

#게시물 전체 조회
class ContentList(APIView):
    queryset = Content.objects.all()
    serializer_class = ContentListSerializer
    # parser_classes = (MultiPartParser, FormParser) #parser

    def get(self, request, **kwargs):
        file_queryset = Content.objects.all()
        serializer = ContentListSerializer(file_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 게시물 생성
class ContentCreate(APIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    # parser_classes = (MultiPartParser, FormParser) #parser
    
    def post(self, request, user_id, **kwargs):
        ## 파일 제목 설정
        # data = request.data.copy()
        # now = datetime.datetime.now()
        # data['attached'].name = now.strftime('%Y-%m-%d %H:%M:%S')+'.pdf'

        # serializer = ContentSerializer(data = data)

        user_profile = UserProfile.objects.get(pk=user_id)
        data1 = request.data.copy()
        data1['user'] = user_profile.user_id

        serializer = ContentSerializer(data=data1)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#특정게시물 조회
class ContentDetail(APIView):
    def get_object(self, post_id):
        content = get_object_or_404(Content, pk=post_id)
        return content
    
    def get(self, request, post_id):
        content = self.get_object(post_id)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

#특정 게시물 수정  
class ContentUpdate(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, post_id):
        content = get_object_or_404(Content, pk=post_id)
        return content
    
    def put(self, request, post_id):
        content = self.get_object(post_id)
        serializer = ContentSerializer(content, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#특정 게시물 삭제
class ContentDelete(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, post_id):
        content = get_object_or_404(Content, pk=post_id)
        return content
    
    def delete(self, request, post_id):
        course = self.get_object(post_id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
#특정 게시물에 댓글 달기
class CommentCreate(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request, post_id, user_id):
        content = Content.objects.get(pk=post_id)
        user_profile = UserProfile.objects.get(pk=user_id)

        data1 = request.data.copy()
        data1['comment_user'] = user_profile.user_id
        data1['content_num'] = content.id #수정
            
        serializer = CommentSerializer(data=data1)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            content.comment_cnt += 1
            content.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 특정 게시물의 댓글 조회
class CommentList(APIView):
	# authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, post_id):
        comments = Comment.objects.filter(content_num=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)



#특정 댓글 조회, 수정, 삭제    
class CommentDetail(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsOwnerOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        return comment
    
    def get(self, request, post_id, comment_id):
        comment = self.get_object(pk=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def put(self, request, post_id, comment_id):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id, comment_id):
        content = Content.objects.get(pk=post_id)
        comment = self.get_object(comment_id)
        comment.delete()
        content.comment_cnt -= 1
        content.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


#게시물 검색 (제목, 내용)
@api_view(['GET'])
def search(request, search):
    contents = Content.objects.filter(Q(title__contains = search)|Q(body__contains = search))
    if contents.exists():
        serializer = ContentListSerializer(contents, many=True)
        return Response(serializer.data)
    else:
        return Response("No result")
    
# #게시물 필터링 (기술스택)
@api_view(['GET'])
def filter(request, search_stack):
    contents = Content.objects.filter(stack__in = [search_stack]) #stack 데이터타입 보고 수정 예정
    if contents.exists():
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data)
    else:
        return Response("No result")


#---------아래는 User모델 추가 후 주석풀기 필요--------------------
#좋아요 달기
@api_view(['POST'])
def like(request, post_id, user_id):
    content = Content.objects.get(pk=post_id)
    user = UserProfile.objects.get(pk=user_id)
    
    if content.like_users.filter(pk=user.user_id).exists(): #테스트필요.. pk가 맞나
        content.like_users.remove(user)
        content.like_cnt -= 1
        content.save()
        return Response(status=status.HTTP_200_OK)
    else:
        content.like_users.add(user)
        content.like_cnt += 1
        content.save()
        return Response(status=status.HTTP_200_OK)

#스크랩하기
@api_view(['POST'])
def scrap(request, post_id, user_id):
    content = Content.objects.get(pk=post_id)
    user = UserProfile.objects.get(pk=user_id)
    
    if content.scrap_users.filter(pk=user.user_id).exists(): #테스트 필요
        content.scrap_users.remove(user)
        content.scrap_cnt -= 1
        content.save()
        return Response(status=status.HTTP_200_OK)
    else:
        content.scrap_users.add(user)
        content.scrap_cnt += 1
        content.save()
        return Response(status=status.HTTP_200_OK)
    
#특정 유저가 작성한 글 조회
@api_view(['GET'])
def content_with_user(request, user_id):
    user = UserProfile.objects.get(pk=user_id) 
    contents = Content.objects.filter(user=user) 
    serializer = ContentListSerializer(contents, many=True)
    return Response(serializer.data)

#특정 유저가 좋아요한 글 조회
@api_view(['GET'])
def likes_with_user(request, user_id):
    user = UserProfile.objects.get(pk=user_id)
    serializer = LikesWithUserSerializer(user)
    return Response(serializer.data)
    
#특정 유저가 스크랩한 글 조회
@api_view(['GET'])
def scraps_with_user(request, user_id):
    user = UserProfile.objects.get(pk=user_id)
    serializer = ScrapsWithUserSerializer(user)
    return Response(serializer.data)