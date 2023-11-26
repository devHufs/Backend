from django.contrib import admin
from django.urls import path, include
from .import views

# http://127.0.0.1:8000/accounts/google/login -> 로그인 페이지


# urlpatterns = [
#    # path('google/signup/', ),
#    # path('google/logout/', ),
#    # path('google/login/', ),
#     path('userinfo/', views.UserRegistration.as_view()),
# ]