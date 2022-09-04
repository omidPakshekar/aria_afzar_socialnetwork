from django.urls import path
from django.urls import path, re_path, include

from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
     TokenObtainPairView,
     TokenRefreshView,
     TokenVerifyView
)
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ConfirmEmailView, ResendEmailVerificationView
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

from payment.api.views import PaymentViewSet
from .views import *



router = DefaultRouter()
router.register('', UserViewSet, basename='')

app_name = 'users_api'
urlpatterns = [
    # path('register/', views.RegistrationView.as_view(), name='register'),
    # path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    # path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('wallet/', WalletView.as_view(), name='wallet'),
    path('membership/', MembershipView.as_view(), name='membership'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('custom-userid/', CustomUserIdApiView.as_view(), name='create-custom-userid' ),
    path('check-userid/', CheckUserIdApiView.as_view(), name='check-custom-userid' ),
    path('register/', RegisterView.as_view()),
    path('login/', CustomUserLogin.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change-password/', PasswordChangeView.as_view(), name='password_change'),
    path('verify-email/', CustomVerifyEmail.as_view(), name='verify-email'),
    path('registration/resend-email/', ResendEmailVerificationView.as_view(), name='resend-email-verification'),
#     path('verify-email/',
#          VerifyEmailView.as_view(), name='rest_verify_email'),
#     path('account-confirm-email/',
#          VerifyEmailView.as_view(), name='account_email_verification_sent'),
#     re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
#             VerifyEmailView.as_view(), name='account_confirm_email'),
     path('password-reset/', PasswordResetView.as_view()),
     path('password-reset-confirm/<slug:uidb64>/<slug:token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
     path('change-bio/', UpdateBioView.as_view(), name='change-bio'),
     path('change-profile-image/', UpdateProfilePicView.as_view(), name='change-profile-image'),
     
     path('', include(router.urls)),
     

]

