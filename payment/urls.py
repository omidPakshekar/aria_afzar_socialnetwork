from django.contrib import admin
from django.urls import path, include

from . import views

app_name='payment'
urlpatterns = [
    path('create/', views.PaymentCreateView.as_view(), name='payment-create'),
    path('update/<int:pk>/', views.ChangePaymentStatus.as_view(), name='change-status'),
    path('history/', views.PaymentHistoryView.as_view(), name='payment-history')

]