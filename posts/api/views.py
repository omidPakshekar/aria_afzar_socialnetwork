import json
from datetime import timedelta
from decimal import Decimal
from urllib import request

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
from posts.api.permissions import PostPermission, ProjectPermission
from payment.models import TransactionHistory


user_admin = CustomeUserModel.objects.get(id=1)

def add_activity(piggy, user):
    activity, _ = Activity.objects.get_or_create(piggy=piggy, user=user)
    activity.number += 1
    activity.save()
            
def add_money(owner, user, amount, kind):
    piggy = owner.user_piggy.filter( Q(started_time__lte=timezone.now()) )[0]
    piggyLong = owner.user_piggy.filter(long=True)[0]
    if piggy.amount > amount:
        w = Wallet.objects.get(id=user.id)
        w.amount += Decimal(amount)
        w.save()    
        TransactionHistory.objects.create(owner=user, amount=amount, kind=kind)
        TransactionHistory.objects.create(owner=owner, amount=-1*amount, kind='piggy')
        piggy.amount = piggy.amount - Decimal(amount)
        piggy.save()
        add_activity(piggy, user)
        add_activity(piggyLong, user)
        

def calculte_period(period, objects):
    if period =='daily':
        return objects.filter(created_time__gte=timezone.now() - timedelta(hours=24))
    elif period =='weekly':
        return objects.filter(created_time__gte=timezone.now() - timedelta(days=7))
    elif period == 'monthly':
        return objects.filter(created_time__gte=timezone.now() - timedelta(days=30))        
    return objects.filter(created_time__gte=timezone.now() - timedelta(days=365))

class ObjectMixin:
    list_serializer = None
    admin_check_serializer = None
    model_ = None
    def get_queryset(self):
        try:
            if  self.request.user.is_admin:
                return self.model_.objects.all()
        except: pass
        return self.model_.objects.filter(admin_check=True) | self.model_.objects.filter(owner=self.request.user)

    # every time user update the model admin_check = False
    def perform_update(self, serializer):
        if self.request.user.is_admin:
            serializer.save(admin_check=True)
        else:
            serializer.save(admin_check=False)

    @action(methods=["put"], detail=True, name="user liked", url_path='like')
    def add_like(self, request, pk):
        instance = self.get_object()
        # add if 
        if self.request.user in instance.user_liked.all() or self.request.user == instance.owner:
            return Response(status.HTTP_200_OK)
        instance.user_liked.add(self.request.user)
        # if user is admin dont do anything
        if self.request.user.is_admin:
            return Response(status.HTTP_200_OK)
        # user member ship --> add money
        # cost money and add to admin if user dosent have member ship
        if self.request.user.have_membership:
            add_money(self.request.user, instance.owner, 0.01, kind='like')
        else:
            add_money(self.request.user, user_admin, 0.01, kind='like')
        return Response(status.HTTP_200_OK)
    
    @action(methods=["put"], detail=True, name="user saved", url_path='save')
    def add_user_saved(self, request, pk):
        instance = self.get_object()
        instance.user_saved.add(self.request.user)
        return Response(status.HTTP_200_OK)

    @action(methods=["post"], detail=True, name="add comment", url_path='add-comment')
    def add_comment(self, request, pk):
        instance = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, item=instance)    
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)
    
    @action(methods=["get"], detail=False, name="admin_check", url_path='admin-check')
    def admin_check(self, request):
        objects_ = self.model_.objects.filter(admin_check=False)
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response(self.admin_check_serializer(page, many=True, context={"request": request}).data) 
        serializer = self.admin_check_serializer(objects_, many=True, context={"request": request})
        return Response(serializer.data)
    
    @action(methods=["put"], detail=True, name="admin_accpet", url_path='admin-accept')
    def admin_accept(self, request, pk):
        """
            only admin can change admin_checked field
        """
        instance = self.get_object()
        instance.admin_check = True
        instance.save()
        return Response(status.HTTP_200_OK)
    
    @action(methods=["get"], detail=False, name="user Item created", url_path='mine')
    def mine(self, request):
        objects_ = self.model_.objects.filter(owner=request.user)
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response( self.list_serializer(page, many=True, context={"request": request}).data )
        serializer = self.list_serializer(objects_, many=True, context={"request": request})
        return Response(serializer.data)
    @action(methods=["get"], detail=False, name="user Item created", url_path='mine/count')
    def mine_count(self, request):
        count = self.model_.objects.filter(owner=request.user).count()
        return Response({
                'number' : count
            })
        

    @action(methods=["get"], detail=True, name="get_comment", url_path='get-comment')
    def get_comment(self, request, pk):
        instance = self.get_object()
        serializer = CommentInlineSerializer(instance = instance.comment.all(), many=True)
        return Response(serializer.data)

    # @action(methods=["get"], detail=False, name="count", url_path='count')
    # def get_count(self, request):
    #     queryset = self.get_queryset()
    #     daily =  queryset.filter(created_time__gte=timezone.now() - timedelta(hours=24))
    #     weekly = queryset.filter(created_time__gte=timezone.now() - timedelta(days=7))
    #     monthly = queryset.filter(created_time__gte=timezone.now() - timedelta(days=30))
    #     yearly = queryset.filter(created_time__gte=timezone.now() - timedelta(days=365))
    #     data = {
    #         'count' : queryset.count(),
    #         'number_in_day': daily.count(),
    #         'number_in_week': weekly.count(),
    #         'number_in_month': monthly.count(),
    #         'number_in_year': yearly.count(),
    #     }
    #     return Response((data))   

    @action(methods=["get"], detail=False, name="history", url_path='history')
    def history(self, request):
        if request.user.is_admin:
            objects = self.get_queryset()
        else:
            objects = self.get_queryset().filter(owner=request.user)
        period = request.query_params.get('period', None)
        print(objects)
        if period != None:
            objects = calculte_period(objects=objects, period=period)
        print(objects)
        page = self.paginate_queryset(objects)
        if page is not None:
            return self.get_paginated_response(self.list_serializer(page, many=True, context={"request": request}).data)
        serializer = self.list_serializer(objects, many=True, context={"request": request})
        return Response(serializer.data)
    

    

class ExprienceViewSet(ObjectMixin, viewsets.ModelViewSet):
    """
        get all item --> /exprinece/
        get one item --> /exprinece/<id>/
        get all item that user create --> /exprience/mine/
        create item --> /exprince/
        destory --> /exprince/<id>/
        get all comment for item --> /exprience/id/get-comment/
        add comment for item --> /exprience/id/add-comment/
        like item ---> /exprience/<id>/like/
        save item ---> /exprince/<id>/save/
        accept a item --> only admin can do /exprience/<id>/admin-accept/
    """
    permission_classes = [PostPermission]
    list_serializer = ExprienceSerializer
    admin_check_serializer = ExprienceAdminCheckSerializer
    model_ = SuccessfullExperience

    def get_serializer_class(self):
        if self.action == 'create':
            return ExprienceCreateSerializer
        if self.action in [ 'partial_update', 'update']:
            try:
                if self.request.user.is_admin:
                    return ExprienceAdminUpdateSerializer
            except: pass
            return ExprienceUpdateSerializer
        return ExprienceSerializer

    def perform_create(self, serializer):
        if  self.request.user.is_admin:
            serializer.save(owner=self.request.user, admin_check=True)
        else:
            serializer.save(owner=self.request.user)
    


class PostViewSet(ObjectMixin, viewsets.ModelViewSet):
    """
        get all item --> /post/
        get one item --> /post/<id>/
        get all item that user create --> /post/mine/
        create item --> /post/
        destory --> /post/<id>/
        get all comment for item --> /post/id/get-comment/
        add comment for item --> /post/id/add-comment/
        like item ---> /post/<id>/like/
        save item ---> /post/<id>/save/
        accept a item --> only admin can do /post/<id>/admin-accept/
    """
    permission_classes = [PostPermission]
    list_serializer = PostSerializer
    admin_check_serializer = PostAdminCheckSerializer
    model_ = Post


    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        if self.action in [ 'partial_update', 'update']:
            try:
                if self.request.user.is_admin:
                    return PostAdminUpdateSerializer
            except: pass
            return PostUpdateSerializer
        return PostSerializer

    def perform_create(self, serializer):
        if  self.request.user.is_admin:
            serializer.save(owner=self.request.user, admin_check=True)
        else:
            serializer.save(owner=self.request.user)

class PodcastViewSet(ObjectMixin, viewsets.ModelViewSet):
    """
        get all item --> /podcast/
        get one item --> /podcast/<id>/
        get all item that user create --> /podcast/mine/
        create item --> /podcast/
        destory --> /podcast/<id>/
        get all comment for item --> /podcast/id/get-comment/
        add comment for item --> /podcast/id/add-comment/
        like item ---> /podcast/<id>/like/
        save item ---> /podcast/<id>/save/
        accept a item --> only admin can do /podcast/<id>/admin-accept/
    """

    permission_classes = [PostPermission]
    list_serializer = PodcastSerializer
    admin_check_serializer = PodcastAdminCheckSerializer
    model_ = Podcast

    def get_serializer_class(self):
        if self.action == 'create':
            return PodcastCreateSerializer
        if self.action in [ 'partial_update', 'update']:
            try:
                if self.request.user.is_admin:
                    return PodcastAdminUpdateSerializer
            except: pass
            return PodcastUpdateSerializer
        return PodcastSerializer

    def perform_create(self, serializer):
        if  self.request.user.is_admin:
            serializer.save(owner=self.request.user, admin_check=True)
        else:
            serializer.save(owner=self.request.user)
            
    @action(methods=["post"], detail=True, name="listen", url_path='listen')
    def add_listen(self, request, pk):
        instance = self.get_object()
        if self.request.user == instance.owner or self.request.user.is_admin or not self.request.user.have_membership:
            return Response(status.HTTP_200_OK)
        add_money(request.user, instance.owner, 0.1, kind='listen')
        return Response(status.HTTP_200_OK)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [ProjectPermission]
    serializer_class = ProjectCreateSerializer
    def get_serializer_class(self):
        return super().get_serializer_class()

    @action(methods=["put"], detail=True, name="add request", url_path='add-request')
    def add_request(self, request, pk):
        instance = self.get_object()
        instance.requests.add(self.request.user)
        return Response(status.HTTP_200_OK)
    
    @action(methods=["get"], detail=True, name="show all request for project", url_path='show-request')
    def show_requests(self, request, pk):
        instance = self.get_object().requests.all()
        return Response(UserInlineSerializerNonAdmin(instance=instance, context={"request": request}, many=True).data)
    




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


