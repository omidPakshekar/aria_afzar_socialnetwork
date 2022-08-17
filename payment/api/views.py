from rest_framework import generics, viewsets

from . import serializers
from ..models import Payment
from rest_framework.permissions import IsAuthenticated

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.PaymentListSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.PaymentCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




























