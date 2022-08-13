
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import confirm_email

from homepage.views import index

urlpatterns = [
    path('', index, name='home'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('payment/', include('payment.urls')),
    
    # path(
    #     "accounts-rest/registration/account-confirm-email/<str:key>/",
    #     confirm_email,
    #     name="account_confirm_email",
    # ),
]

if settings.DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
