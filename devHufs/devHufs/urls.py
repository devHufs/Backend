from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('allauth.urls')),
    path('api/accounts/', include('accounts.urls')),
    #path('accounts/', include('accounts.urls')),
    # path('mypage/', include('mypage.urls')),
    # path('', include('iamport.urls')),
    # path('', include('store.urls')),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)