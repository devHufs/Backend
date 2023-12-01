import os
from django.shortcuts import redirect
from json import JSONDecodeError
from django.http import JsonResponse
import requests
from rest_framework import status
from .models import *
from allauth.socialaccount.models import SocialAccount
from dotenv import load_dotenv
load_dotenv()


##### 백에서 직접 엑세스 토큰 + 이메일 얻음 #####

state = os.environ.get("STATE")
# BASE_URL = 'http://localhost:8000/'
BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/accounts/google/callback/'


# 구글 로그인
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.getenv("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    #os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


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


def get_id_token(access_token):
    google_user_api = GoogleUserApi(base_url="https://www.googleapis.com")
    status_code, response_text = google_user_api.get_user_info(access_token)

    if status_code == 200:
        print(f"Success! User Info: {response_text}")
    else:
        print(f"Failed with status code {status_code}")


def google_callback(request):
    client_id = os.getenv("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.getenv("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')

    # 1. 받은 코드로 구글에 access token 요청
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    
    ### 1-1. json으로 변환 & 에러 부분 파싱
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    ### 1-2. 에러 발생 시 종료
    if error is not None:
        raise JSONDecodeError(error)

    ### 1-3. 성공 시 access_token 가져오기
    access_token = token_req_json.get('access_token')

    #################################################################

    # 2. 가져온 access_token으로 이메일값을 구글에 요청
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code

    ### 2-1. 에러 발생 시 400 에러 반환
    if email_req_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
    ### 2-2. 성공 시 이메일 가져오기
    email_req_json = email_req.json()
    email = email_req_json.get('email')

    get_id_token(access_token)

    return JsonResponse({'access': access_token, 'email':email})










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

#     # 이미 Google로 제대로 가입된 유저 => 로그인 & 해당 유저의 jwt 발급
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
        
# 	# except SocialAccount.DoesNotExist:
#     # 	# User는 있는데 SocialAccount가 없을 때 (=일반회원으로 가입된 이메일일때)
#     #     return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)


from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client































##### 프론트에서 받아 검증 요청 #####

# email_req = requests.get(
# f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
# email_req_status = email_req.status_code

# if email_req_status != 200:
#     return JsonResponse({'err_msg': 'failed to get email'},status=status.HTTP_400_BAD_REQUEST)
# email_req_json = email_req.json()
# email = email_req_json.get('email')


# """
# 전달받은 email, access token 바탕으로 회원가입/로그인
# """
# try:
#     user = User.objects.get(email=email)
#     # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
#     # 다른 SNS로 가입된 유저
#     social_user = SocialAccount.objects.get(user=user)
#     if social_user is None:
#         return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
#     if social_user.provider != 'google':
#         return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
#     # 기존에 Google로 가입된 유저
#     data = {'access_token': access_token, 'code': code}
#     accept = requests.post(
#         f"{BASE_URL}accounts/google/login/finish/", data=data)
#     accept_status = accept.status_code
#     if accept_status != 200:
#         return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
#     accept_json = accept.json()
#     accept_json.pop('user', None)
#     return JsonResponse(accept_json)
# except User.DoesNotExist:
#         # 기존에 가입된 유저가 없으면 새로 가입
#     data = {'access_token': access_token, 'code': code}
#     accept = requests.post(
#         f"{BASE_URL}accounts/google/login/finish/", data=data)
#     accept_status = accept.status_code
#     if accept_status != 200:
#         return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
#     accept_json = accept.json()
#     accept_json.pop('user', None)
#     return JsonResponse(accept_json)



''''''
{
    "access": "ya29.a0AfB_byDUCivbgn-_jiNE0yXlyeXyNDPgWRWEM6jldy3nrcWbV9_21lJq2By1BLSoD0AYy7jAXEZUtPjml4gGwFNa-PcZjdu5f1O5pXBSmPfyaRVLVmkAVjaCrhexrVQ4HDhfFjhMMdWJGR2YVk8ncxBNz5dyOoT149JTaCgYKAVESARMSFQHGX2MiGjC-haItF9Ez-M4fEQjj0A0171",
    "email": "hyobin3026@hufs.ac.kr"
}
''''''