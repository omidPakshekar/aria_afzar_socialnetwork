from datetime import timedelta
from decimal import Decimal

from django.db.models import Q
from django.utils import timezone

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action 
from rest_framework.response import Response
from rest_framework import status

from .serializers import ExprienceCreateSerializer, ExprienceSerializer
from ..models import SuccessfullExperience
from users.models import Activity, CustomeUserModel, add_to_admin_wallet, Wallet
from posts.api.permissions import PostPermission

user_admin = CustomeUserModel.objects.get(id=1)

def add_money(owner, user, amount, trade_off):
    piggy = owner.user_piggy.filter( Q(started_time__gte=timezone.now() )  )[0]
    piggyLong = owner.user_piggy.filter(long=True)[0]
    print('**'*10)
    print(piggyLong)
    print('**'*10)
    if piggy.amount > amount:
        w = Wallet.objects.get(id=user.id)
        w.amount += Decimal(amount)
        w.save()
        piggy.amount = piggy.amount - Decimal(amount)
        piggy.save()

        try:
            activity = Activity.objects.get(piggy=piggy)
            activity.number += 1
            activity.save()
            activity2 = Activity.objects.get(piggy=piggyLong)
            activity2.number += 1
            activity2.save()
        except:
            activity = Activity.objects.create(piggy=piggy, user=user)
            activity.number += 1
            activity.save()
            activity2 = Activity.objects.create(piggy=piggyLong, user=user)
            activity2.number += 1
            activity2.save()
            
        
class ExprienceViewSet(viewsets.ModelViewSet):
    queryset = SuccessfullExperience.objects.all()
    permission_classes = [PostPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return ExprienceCreateSerializer
        return ExprienceSerializer

    def perform_create(self, serializer):
        if  self.request.user.is_admin:
            serializer.save(owner=self.request.user, admin_check=True)
        else:
            serializer.save(owner=self.request.user)

    # @action(methods=["put"], detail=True, name="change status", url_path='change-status')
    # def change_status(self, request, pk):
    #     instance = self.get_object()
    #     serializer = ExprienceChangeSerializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)

    @action(methods=["put"], detail=True, name="user liked", url_path='like')
    def add_like(self, request, pk):
        instance = self.get_object()
        # add if 
        instance.user_liked.add(self.request.user)
        # user member ship --> add money
        # cost money and add to admin if user dosent have member ship
        if self.request.user.have_membership:
            add_money(self.request.user, instance.owner, 0.01, 0)
        else:
            add_money(self.request.user, user_admin, 0.01, 0)

        return Response(status.HTTP_200_OK)
    
    @action(methods=["put"], detail=True, name="user saved", url_path='save')
    def add_user_saved(self, request, pk):
        instance = self.get_object()
        instance.user_saved.add(self.request.user)
        return Response(status.HTTP_200_OK)






