from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required

from . import views

app_name='users'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/wallet/', views.WalletView.as_view(), name='wallet'),
    path('profile/<slug:slug>/', views.ProfileView.as_view(), name='customers-slug'),

]    