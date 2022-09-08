from django.urls import path, include
from .views import CommentLikeApiView

app_name = 'post_api'
urlpatterns = [
    path('<int:pk>/like/', CommentLikeApiView.as_view(), name='comment-like')
]