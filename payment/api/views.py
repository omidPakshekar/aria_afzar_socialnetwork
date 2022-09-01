from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action 
from rest_framework.response import Response

from . import serializers
from . import permissions
from ..models import Payment, TransactionHistory

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
        # get data and validated 
        instance = self.get_object()
        serializer = serializers.PaymentChangeStatus(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
   
    @action(methods=["get"], detail=False, name="payment that create by the logged in user")
    def mine(self, request):
        objects = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(objects)
        if page is not None:
            serializer = serializers.PaymentListSerializer(page, many=True, context={"request": request})
        serializer = serializers.PaymentListSerializer(objects, many=True, context={"request": request})
        return Response(serializer.data)

    

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = TransactionHistory.objects.all()
    # permission_classes = [permissions.TransactionPermission]
    serializer_class = serializers.TransactionHistorySerializer










    
    # @action(methods=["post"], detail=False, name="Posts by the logged in user")
    # def donate(self, request):    
    

# partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
