from django.contrib import admin
from django.urls import path, include
from .views import *

##### 백에서 직접 엑세스 토큰 + 이메일 얻음 #####
urlpatterns = [
    path('google/login', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    path('google/login/get_id_token/', get_id_token, name='get_id_token'),
]
