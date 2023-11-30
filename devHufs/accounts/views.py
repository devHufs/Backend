# from .models import *
# from rest_framework import status
# from rest_framework.views import View
# from rest_framework.response import Response
# import requests
# import jwt
# from django.http import JsonResponse
# from dotenv import load_dotenv
# import os
# from django.conf import settings


# class GoogleLoginView(View):
#     def get(self, request, *args, **kwargs):
#         token = request.headers["Authorization"]
#         #url = 'https://oauth2.googleapis.com/tokeninfo?id_token='
#         url = 'https://oauth2.googleapis.com/tokeninfo?access_token='
#         response = requests.get(url + token)
#         user = response.json()
#         user_sub = user.get('sub', None)

#         wef_key = settings.SECRET_KEY

#         none_member_type = 1  # none_member_type 변수 정의

#         if User.objects.filter(social_login_id=user_sub).exists():
#             user_info = User.objects.get(social_login_id=user_sub)
#             encoded_jwt = jwt.encode({'id': user_sub}, wef_key, algorithm='HS256')

#             return JsonResponse({
#                 'access_token': encoded_jwt.decode('UTF-8'),
#                 'user_name': user['name'],
#                 'user_type': none_member_type,
#                 'user_pk': user_info.id
#             }, status=200)
        
#         else:
#             new_user_info = User(
#                 social_login_id=user_sub,
#                 name=user['name'],
#                 social=GoogleLogin.objects.get(platform="google"),
#                 email=user.get('email', None)
#             )
#             new_user_info.save()
#             encoded_jwt = jwt.encode({'id': new_user_info.id}, wef_key, algorithm='HS256')

#             return JsonResponse({
#                 'access_token': encoded_jwt.decode('UTF-8'),
#                 'user_name': new_user_info.name,
#                 'user_type': none_member_type,
#                 'user_pk': new_user_info.id,
#             }, status=200)
        
# # import requests
# # from django.http import JsonResponse
# # from django.views import View
# # from django.conf import settings


# # class GoogleLoginView(View):
# #     def get(self, request, *args, **kwargs):
# #         oauth_token = request.GET.get('oauthToken')  # Assuming the token is passed as a query parameter
# #         user_info = self.get_sns_user_model(oauth_token)
# #         return JsonResponse({
# #             'sub': user_info.sub,
# #             'name': user_info.name,
# #             'given_name': user_info.given_name,
# #             'family_name': user_info.family_name,
# #             'picture': user_info.picture,
# #             'email': user_info.email,
# #             'email_verified': user_info.email_verified,
# #             'locale': user_info.locale,
# #         })

#     # def get_sns_user_model(self, oauth_token):
#     #     user_api_google = "https://openidconnect.googleapis.com/v1/userinfo?access_token="
#     #     headers = {
#     #         'Authorization': f'Bearer {oauth_token}'
#     #     }
#     #     response = requests.get(user_api_google + oauth_token, headers=headers)

#     #     if response.status_code == 200:
#     #         user_data = response.json()
#     #         user_model = UserModel(
#     #             sub=user_data.get('sub', None),
#     #             name=user_data.get('name', None),
#     #             given_name=user_data.get('given_name', None),
#     #             family_name=user_data.get('family_name', None),
#     #             picture=user_data.get('picture', None),
#     #             email=user_data.get('email', None),
#     #             email_verified=user_data.get('email_verified', False),
#     #             locale=user_data.get('locale', None),
#     #         )
#     #         return user_model
#     #     else:
#     #         # Handle error, you might want to raise an exception or return a default UserModel
#     #         pass



import os
from django.shortcuts import redirect
from json import JSONDecodeError
from django.http import JsonResponse
import requests
import os
from rest_framework import status
from .models import *
from allauth.socialaccount.models import SocialAccount

state = os.environ.get("STATE")
# BASE_URL = 'http://localhost:8000/'
BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/accounts/google/callback/'

# client_id = '737061732619-j4odeagmc041qbsakpu0jlljvetroqaa.apps.googleusercontent.com'

# 구글 로그인
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = "737061732619-j4odeagmc041qbsakpu0jlljvetroqaa.apps.googleusercontent.com"
    #os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    client_id = "737061732619-j4odeagmc041qbsakpu0jlljvetroqaa.apps.googleusercontent.com"
    #os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = "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"
    #os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
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

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google import views as google_view

class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client