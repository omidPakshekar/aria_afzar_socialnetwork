import json
from multiprocessing import context
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from decimal import Decimal

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action 
from rest_framework.response import Response
from rest_framework import status, generics
from users.api.serializers import UserInlineSerializerNonAdmin, UserSeenInfoSerializer

from users.models import Activity

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
            return self.get_paginated_response(serializer = serializers.PaymentListSerializer(page, many=True, context={"request": request}).data)
        serializer = serializers.PaymentListSerializer(objects, many=True, context={"request": request})
        return Response(serializer.data)
    

        

    

class TransactionViewSet(viewsets.ModelViewSet):
    """
        withdraw ---> if you are admin you can see all withdraw  if your regular user
                    you can see your withdraw  --> get /transaction/withdraw/  ---> all transaction
                                                    /transaction/withdraw/?period=daily or weekly or monthly or yearly
    """
    queryset = TransactionHistory.objects.all()
    permission_classes = [permissions.TransactionPermission]
    serializer_class = serializers.TransactionHistorySerializer
    
    def get_objects(self, objects, period):
        if period =='daily':
            return objects.filter(created_time__gte=timezone.now() - timedelta(hours=24))
        elif period =='weekly':
            return objects.filter(created_time__gte=timezone.now() - timedelta(days=7))
        elif period == 'monthly':
            return objects.filter(created_time__gte=timezone.now() - timedelta(days=30))
        return objects.filter(created_time__gte=timezone.now() - timedelta(days=365))
    
    @action(methods=["get"], detail=False, name="withdraw", url_path='withdraw')
    def withdraw(self, request):
        if request.user.is_admin:
            objects = self.get_queryset().filter(kind='withdraw')
        else:
            objects = self.get_queryset().filter(owner=request.user).filter(kind='withdraw')
        period = request.query_params.get('period', None)
        if period != None:
            objects = self.get_objects(objects=objects, period=period)
        page = self.paginate_queryset(objects)
        if page is not None:
            return self.get_paginated_response(self.serializer_class(page, many=True, context={"request": request}).data)
        serializer = self.serializer_class(objects, many=True, context={"request": request})
        return Response(serializer.data)
    
    @action(methods=["get"], detail=False, name="withdraw", url_path='deposit')
    def deposit(self, request):
        if request.user.is_admin:
            objects = self.get_queryset().filter(kind='deposit')
        else:
            objects = self.get_queryset().filter(owner=request.user).filter(kind='deposit')
        period = request.query_params.get('period', None)
        if period != None:
            objects = self.get_objects(objects=objects, period=period)
        page = self.paginate_queryset(objects)
        if page is not None:
            return self.get_paginated_response(self.serializer_class(page, many=True, context={"request": request}).data)
        serializer = self.serializer_class(objects, many=True, context={"request": request})
        return Response(serializer.data)
    @action(methods=["get"], detail=False, name="withdraw", url_path='income')
    def income(self, request):
        objects = self.get_queryset().filter(owner=request.user)
        period = request.query_params.get('period', None)
        if period != None:
            objects = self.get_objects(objects=objects, period=period)
            print(objects)
        return Response(objects.aggregate(Sum('amount')))

    @action(methods=["get"], detail=False, name="money box", url_path='moneybox')
    def money_box(self, request):
        activity = Activity.objects.filter(user=self.request.user)
        lst= []
        for i in activity:
            piggy = i.piggy
            number =  Activity.objects.filter(piggy=piggy).aggregate(Sum('number'))['number__sum']
            money_unit = piggy.amount / number  
            user_money = float(i.number * money_unit)
            seconds = piggy.day_left.total_seconds()
            days = seconds // (3600 * 24)
            hours = (seconds // 3600) % 24
            minutes = (seconds // 60) % 60
            seconds = seconds % 60
            lst.append({
                "time_left": '{} minutes, {} hours, {} days'.format(minutes, hours, piggy.day_left.days),
                "number_of_user": number,
                "money_unit" : float(money_unit),
                "user_money" : user_money,
                "moneybox_owner": UserSeenInfoSerializer(instance=piggy.user, context={'request': request}).data
            })
        return Response(lst, status=status.HTTP_200_OK)

    #     if request.user.is_admin:
    #         objects = self.get_queryset().filter(kind='withdraw')
    #     else:
    #         objects = self.get_queryset().filter(user=request.user).filter(kind='withdraw')
    #     page = self.paginate_queryset(objects)
    #     if page is not None:
    #         return self.get_paginated_response(serializer = serializers.PaymentListSerializer(page, many=True, context={"request": request}).data)
    #     serializer = serializers.PaymentListSerializer(objects, many=True, context={"request": request})
    #     return Response(serializer.data)
        

# class IncomeViewSet(generics.ListAPIView):
#     queryset = TransactionHistory.objects.all()
#     def list(self, request, *args, **kwargs):
#         period = request.query_params.get('period', None)
#         if period == 'daily':
#             pass
#         elif period =='weekly':
#             pass
#         self.queryset = TransactionHistory.objects.filter()
#         return super().list(request, *args, **kwargs)



  




    
    # @action(methods=["post"], detail=False, name="Posts by the logged in user")
    # def donate(self, request):    
    

# partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
