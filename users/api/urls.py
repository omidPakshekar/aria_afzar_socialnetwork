from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

app_name = 'users_api'
urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),

    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('wallet/', views.WalletView.as_view(), name='wallet'),
    path('membership/', views.MembershipView.as_view(), name='membership'),

]