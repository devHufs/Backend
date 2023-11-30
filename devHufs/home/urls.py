from django.urls import path
from . import views
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', ContentList.as_view()),
    path('create/', ContentList.as_view(), name='content_create'),
    path('<int:post_id>/', ContentDetail.as_view()),
    path('<int:post_id>/update/', ContentDetail.as_view(), name='content-update'),
    path('<int:post_id>/delete/', ContentDetail.as_view(), name='content-destroy'),
    # path('<int:post_id>/like/<int:user_id>/', like, name='like'),
    # path('<int:post_id>/scrap/<int:user_id>/', scrap, name='scrap'),
    path('<int:post_id>/comment/', CommentList.as_view(), name='comment_create'),
    path('<int:post_id>/comment/<int:comment_id>/', CommentDetail.as_view(), name='comment-updatedestroy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
