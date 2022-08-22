from django.urls import path
from django.urls import path, re_path, include

from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ConfirmEmailView
from dj_rest_auth.views import LoginView, LogoutView

from . import views
from payment.api.views import PaymentViewSet
from .views import UserViewSet

router = DefaultRouter()
router.register('', UserViewSet, basename='')

app_name = 'users_api'
urlpatterns = [
    # path('register/', views.RegistrationView.as_view(), name='register'),
    # path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    # path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    # path('wallet/', views.WalletView.as_view(), name='wallet'),
    # path('membership/', views.MembershipView.as_view(), name='membership'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/',
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
            VerifyEmailView.as_view(), name='account_confirm_email'),
     path('', include(router.urls)),

]

