from django.contrib import admin
from django.urls import path, include

from . import views

app_name='payment'
urlpatterns = [
    path('', views.PaymentCreateView.as_view(), name='payment'),
    path('update/<int:pk>/', views.ChangePaymentStatus.as_view(), name='change-status'),

]