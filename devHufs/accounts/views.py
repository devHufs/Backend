import os
from django.shortcuts import redirect
import requests
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


##### 백에서 직접 엑세스 토큰 + 이메일 얻음 #####

state = os.environ.get("STATE")
BASE_URL = 'http://127.0.0.1:8000/'
GET_ACCESS_TOKEN_URI = BASE_URL + 'api/accounts/google/login/gettoken/'



class GoogleUserApi:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user_info(self, access_token):
        endpoint = "/userinfo/v2/me"
        url = f"{self.base_url}{endpoint}"
        
        # HTTP GET 요청 보내기
        response = requests.get(url, params={'access_token': access_token})

        # HTTP 응답 코드와 내용 반환
        return response.status_code, response.text


class GetAccessToken(APIView):
    def get(self, request, **kwarg):
        access_token = request.headers.get("Authorization")
        google_user_api = GoogleUserApi(base_url="https://www.googleapis.com")
        status_code, response_text = google_user_api.get_user_info(access_token)

        if status_code == 200:
            user_info = HttpResponse(response_text)
            # user_id = user_info.get("user_id") # 사용자의 고유 식별자 추출
            # #id값 바뀌는지 아닌지 확인, 안 바뀌면 받는 id 그대로 사용 가능할 듯

            # if not UserProfile.objects.filter(user_id=user_id).exists():
            #     UserProfile.objects.create(user_id=user_id, email=user_info.get("email"),
            #                 name=user_info.get("given_name"), pic=user_info.get("picture"))
            
            return user_info
        else:
            return Response(status_code)

## http://127.0.0.1:8000/api/accounts/google/login/get_id_token/
## Headers에 Authorization으로 엑세스 토큰값 넣기

## python3 manage.py runserver 0:8000

# class UserInfo(APIView):
#     def get(self, request, user_id):
#         user = get_object_or_404(UserProfile, id=user_id)
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def patch(self, request, user_id):
#         user = get_object_or_404(UserProfile, id=user_id)
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, user_id):
#         user = get_object_or_404(UserProfile, id=user_id)
#         user.delete()
#         return Response({'message': '삭제됨'}, status=status.HTTP_204_NO_CONTENT)
        