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
            user_info = HttpResponse(response_text)
            if user_info['hd'] == "hufs.ac.kr":
                return user_info
            else:
                return 'hufs 계정 아님'
        else:
            return Response(status_code)

## http://127.0.0.1:8000/api/accounts/google/login/get_id_token/
## Headers에 Authorization으로 엑세스 토큰값 넣기

## 






#################################################################

    # # 3. 전달받은 이메일, access_token, code를 바탕으로 회원가입/로그인
    # try:
    #     # 전달받은 이메일로 등록된 유저가 있는지 탐색
    #     user = User.objects.get(email=email)

    #     # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 있는지 확인
    #     social_user = SocialAccount.objects.get(user=user)

    #     # 있는데 구글계정이 아니어도 에러
    #     if social_user.provider != 'google':
    #         return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

    #     # 이미 Google로 제대로 가입된 유저 => 로그인 & 해당 우저의 jwt 발급
    #     data = {'access_token': access_token, 'code': code}
    #     accept = requests.post(f"{BASE_URL}api/user/google/login/finish/", data=data)
    #     accept_status = accept.status_code

    #     # 뭔가 중간에 문제가 생기면 에러
    #     if accept_status != 200:
    #         return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)

    #     accept_json = accept.json()
    #     accept_json.pop('user', None)
    #     return JsonResponse(accept_json)

    # except User.DoesNotExist:
    #     # 전달받은 이메일로 기존에 가입된 유저가 아예 없으면 => 새로 회원가입 & 해당 유저의 jwt 발급
    #     data = {'access_token': access_token, 'code': code}
    #     accept = requests.post(f"{BASE_URL}api/user/google/login/finish/", data=data)
    #     accept_status = accept.status_code

    #     # 뭔가 중간에 문제가 생기면 에러
    #     if accept_status != 200:
    #         return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

    #     accept_json = accept.json()
    #     accept_json.pop('user', None)
    #     return JsonResponse(accept_json)
        
	# except SocialAccount.DoesNotExist:
    # 	# User는 있는데 SocialAccount가 없을 때 (=일반회원으로 가입된 이메일일때)
    #     return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
