from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    #path('login/google', GoogleLoginView.as_view()),
    path('google/login', google_login, name='google_login'),
    path('google/callback/', google_callback, name='google_callback'),
    path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
]
