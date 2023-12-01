from django.contrib import admin
from django.urls import path, include
from home.views import *

##### 백에서 직접 엑세스 토큰 + 이메일 얻음 #####
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('api/accounts/', include('allauth.urls')),
    path('api/accounts/', include('accounts.urls')),
]

