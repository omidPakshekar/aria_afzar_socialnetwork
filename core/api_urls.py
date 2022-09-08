from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (
            TokenObtainPairView, TokenRefreshView, TokenVerifyView)

from rest_framework.routers import DefaultRouter

from payment.api.views import *
from posts.api.views import *
from users.api.views import SupportMessageViewSet
from chat.api.views import ChatViewSet
from drf_chunked_upload.views import ChunkedUploadView

from users.models import SupportMessage

router = DefaultRouter()
router.register('payment', PaymentViewSet)
router.register('exprience', ExprienceViewSet, basename='exprience')
router.register('post', PostViewSet, basename='post')
router.register('podcast', PodcastViewSet, basename='podcast')
router.register('chat', ChatViewSet, basename='chat')
router.register('transaction', TransactionViewSet, basename='transaction')
router.register('project', ProjectViewSet, basename='project')
router.register('message', SupportMessageViewSet, basename='message')


urlpatterns = [
    # path('test/', ChunkedUploadView.as_view()),
    path('accounts/', include('users.api.urls')),
    path('comment/', include('posts.api.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]








