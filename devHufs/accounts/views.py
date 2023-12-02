import os
from django.shortcuts import redirect
import requests
from rest_framework import status
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse


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
            return HttpResponse(response_text)
        else:
            return Response(status_code)

## http://127.0.0.1:8000/api/accounts/google/login/get_id_token/
## Headers에 Authorization으로 엑세스 토큰값 넣기


