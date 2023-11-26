from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', goologin.views.home, name='home')
    path('accounts/', include('allauth.urls')),
]
