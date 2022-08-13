from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required

from . import views

app_name='users'
urlpatterns = [
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('profile/<slug:slug>/', login_required(views.ProfileView.as_view()), name='customers-slug')

]    