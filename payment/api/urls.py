from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('payment', views.PaymentViewSet)

app_name = 'payment_api'
urlpatterns = [
    path('', include(router.urls)),

]