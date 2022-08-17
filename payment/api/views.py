from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action 
from rest_framework.response import Response

from . import serializers
from . import permissions
from ..models import Payment

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [permissions.PaymentPermission]
    serializer_class = serializers.PaymentListSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.PaymentCreateSerializer
        elif self.action == 'change-status':
            return serializers.PaymentChangeStatus
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(methods=["put"], detail=True, name="change status", url_path='change-status')
    def change_status(self, request, pk):
        instance = self.get_object()
        print('instance=', instance.id)
        serializer = serializers.PaymentChangeStatus(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('view4')
        return Response(serializer.data)

# partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)





















