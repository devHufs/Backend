from django.contrib import admin
from django.urls import path, include
from .views import *

##### 백에서 직접 엑세스 토큰 + 이메일 얻음 #####
urlpatterns = [
    path('google/login/get_id_token/', GetAccessToken.as_view(), name='get_id_token'),
]
