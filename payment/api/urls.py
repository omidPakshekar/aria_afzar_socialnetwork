from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'payment_api_url'
urlpatterns = [
    path('income-history/', views.IncomeHistory.as_view(), name='income-history'),
    
]