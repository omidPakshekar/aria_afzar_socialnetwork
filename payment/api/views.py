from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import permissions
from ..models import Payment

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [permissions.PaymentPermission]
    serializer_class = serializers.PaymentListSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.PaymentCreateSerializer
        elif self.action == 'change-status':
            return serializers.PaymentChangeStatus

        return super().get_serializer_class()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




























