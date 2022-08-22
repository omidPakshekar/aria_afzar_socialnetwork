import json
from datetime import timedelta
from decimal import Decimal

from django.db.models import Q
from django.utils import timezone

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action 
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from ..models import Comment, Podcast, Post, SuccessfullExperience
from users.models import Activity, CustomeUserModel, Wallet
from posts.api.permissions import PostPermission

user_admin = CustomeUserModel.objects.get(id=1)

def add_activity(piggy, user):
    activity, _ = Activity.objects.get_or_create(piggy=piggy, user=user)
    activity.number += 1
    activity.save()
            
def add_money(owner, user, amount, trade_off):
    piggy = owner.user_piggy.filter( Q(started_time__lte=timezone.now()) )[0]
    piggyLong = owner.user_piggy.filter(long=True)[0]
    if piggy.amount > amount:
        w = Wallet.objects.get(id=user.id)
        w.amount += Decimal(amount)
        w.save()
        piggy.amount = piggy.amount - Decimal(amount)
        piggy.save()
        add_activity(piggy, user)
        add_activity(piggyLong, user)
        

class LikeSaveMixin:
    @action(methods=["put"], detail=True, name="user liked", url_path='like')
    def add_like(self, request, pk):
        instance = self.get_object()
        # add if 
        if self.request.user in instance.user_liked.all():
            return Response(status.HTTP_200_OK)
        instance.user_liked.add(self.request.user)
        # if user is admin dont do anything
        if self.request.user.is_admin:
            return Response(status.HTTP_200_OK)
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

    @action(methods=["post"], detail=True, name="add comment", url_path='add_comment')
    def add_comment(self, request, pk):
        instance = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, item=instance)    
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)
    

    @action(methods=["put"], detail=True, name="user saved", url_path='admin-accept')
    def admin_accept(self, request, pk):
        """
            only admin can change admin_checked field
        """
        if not request.user.is_admin:
            return Response(
                            json.dumps({'detail' : 'only admin can do'}),
                            status=status.HTTP_403_FORBIDDEN
                        )
        instance = self.get_object()
        instance.admin_check = True
        instance.save()
        return Response(status.HTTP_200_OK)

# change status and admin 
class ExprienceViewSet(LikeSaveMixin, viewsets.ModelViewSet):
    permission_classes = [PostPermission]

    def get_queryset(self):
        if  self.request.user.is_admin:
            return SuccessfullExperience.objects.all()
        return SuccessfullExperience.objects.filter(admin_check=True)

    def get_serializer_class(self):
        if self.action == 'create':
            return ExprienceCreateSerializer
        if self.action in [ 'partial_update', 'update']:
            if self.request.user.is_admin:
                return ExprienceAdminUpdateSerializer
            else:
                return ExprienceUpdateSerializer
        return ExprienceSerializer

    def perform_create(self, serializer):
        if  self.request.user.is_admin:
            serializer.save(owner=self.request.user, admin_check=True)
        else:
            serializer.save(owner=self.request.user)
    


class PostViewSet(LikeSaveMixin, viewsets.ModelViewSet):
    permission_classes = [PostPermission]

    def get_queryset(self):
        if  self.request.user.is_admin:
            return Post.objects.all()
        return Post.objects.filter(admin_check=True)

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        if  self.request.user.is_admin:
            serializer.save(owner=self.request.user, admin_check=True)
        else:
            serializer.save(owner=self.request.user)

class PodcastViewSet(LikeSaveMixin, viewsets.ModelViewSet):
    permission_classes = [PostPermission]

    def get_queryset(self):
        if  self.request.user.is_admin:
            return Podcast.objects.all()
        return Podcast.objects.filter(admin_check=True)

    def get_serializer_class(self):
        if self.action == 'create':
            return PodcastCreateSerializer
        return PodcastSerializer

    def perform_create(self, serializer):
        if  self.request.user.is_admin:
            serializer.save(owner=self.request.user, admin_check=True)
        else:
            serializer.save(owner=self.request.user)



# class CommentViewSet(LikeSaveMixin, viewsets.ModelViewSet):
#     permission_classes = [PostPermission]

#     def get_queryset(self):
#         if  self.request.user.have_membership:
#             return Comment.objects.all()
#         return Comment.objects.filter(admin_check=True)

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return CommentCreateSerializer
#         return CommentSerializer

#     def perform_create(self, serializer):
#         if  self.request.user.is_admin:
#             serializer.save(owner=self.request.user, admin_check=True)
#         else:
#             serializer.save(owner=self.request.user)


