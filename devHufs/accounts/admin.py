from django.contrib import admin
from .models import GoogleLogin, User

##### 백에서 직접 엑세스 토큰 + 이메일 얻음 #####
admin.site.register(GoogleLogin)
admin.site.register(User)