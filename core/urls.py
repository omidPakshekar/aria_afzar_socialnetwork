from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from allauth.account.views import confirm_email
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from allauth.account.views import confirm_email
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

from homepage.views import index

schema_view = get_schema_view(
   openapi.Info(
      title="Jobfinder API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('', index, name='home'),
    path('accounts/', include('allauth.urls')),
    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    # path("auth/registration/account-confirm-email/<str:key>/",
    #     confirm_email,
    #     name="account_confirm_email",
    # ),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('payment/', include('payment.urls')),
    path('api/v1/', include('core.api_urls')),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<slug:uidb64>/<slug:token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # path(
    #     "accounts-rest/registration/account-confirm-email/<str:key>/",
    #     confirm_email,
    #     name="account_confirm_email",
    # ),

]

if settings.DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


