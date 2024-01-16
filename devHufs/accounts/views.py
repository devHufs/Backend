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
from django.http import JsonResponse
from json import loads


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
    def get(self, request, **kwargs):
        access_token = request.headers.get("Authorization")
        google_user_api = GoogleUserApi(base_url="https://www.googleapis.com")
        status_code, response_text = google_user_api.get_user_info(access_token)

        if status_code == 200:
            user_info = loads(response_text)  # 직접 JSON 파싱
            email = user_info.get("email")

            if not UserProfile.objects.filter(email=email).exists():
                UserProfile.objects.create(
                    email=email,
                    name=user_info.get("given_name"),
                    pic=user_info.get("picture"),
                )

            return JsonResponse(user_info, safe=False)
        else:
            return Response(status_code)

        
class UserInfo(APIView):
    def get(self, request, email):
        user = get_object_or_404(UserProfile, email=email)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, email):
        user = get_object_or_404(UserProfile, email=email)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, email):
        user = get_object_or_404(UserProfile, email=email)
        user.delete()
        return Response({'message': '삭제됨'}, status=status.HTTP_204_NO_CONTENT)