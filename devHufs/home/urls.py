from django.urls import path
from . import views
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', ContentList.as_view()),
    path('create/<int:user_id>/', ContentCreate.as_view(), name='content_create'),
    path('<int:post_id>/', ContentDetail.as_view()),
    path('<int:post_id>/update/', ContentUpdate.as_view(), name='content-update'),
    path('<int:post_id>/delete/', ContentDelete.as_view(), name='content-destroy'),

    path('<int:post_id>/comment/create/<int:user_id>/', CommentCreate.as_view(), name='comment_create'),
    path('<int:post_id>/comment/', CommentList.as_view()),
    path('<int:post_id>/comment/<int:comment_id>/', CommentDetail.as_view(), name='comment-updatedestroy'),

    path('search/<str:search>/', search, name='search'),
    path('filter/<str:search_stack>/', filter, name='filter'),

    # User모델 추가 후 주석 풀기
    path('<int:post_id>/like/<int:user_id>/', like, name='like'),
    path('<int:post_id>/scrap/<int:user_id>/', scrap, name='scrap'),
    path('<int:user_id>/contents/', content_with_user),
    path('<int:user_id>/likes/', likes_with_user),
    path('<int:user_id>/scraps/', scraps_with_user),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
