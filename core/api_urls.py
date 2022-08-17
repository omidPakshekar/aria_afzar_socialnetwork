from django.urls import path, include


urlpatterns = [
    path('accounts/', include('users.api.urls')),
]

