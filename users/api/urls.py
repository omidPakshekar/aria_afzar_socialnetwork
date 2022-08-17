from django.urls import path
from .views import RegistrationView
from rest_framework_simplejwt import views as jwt_views

app_name = 'users_api'
urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),

]