import json, jwt, os
from urllib import request
from django.db.models import Q
from posts.api.serializers import ExprienceSerializer, PodcastSerializer, PostSerializer, ProjectSerializer

from posts.models import Podcast, Post, Project, SuccessfullExperience

from .serializers import UserAllInfoSerializer, UserSeenInfoSerializer
from users.api.permissions import SupportMessagePermission, UserViewSetPermission
from .serializers import *
from ..email import send_verification_email  
from ..models import *
from posts.api.views import calculte_period

from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django_countries.serializers import CountryFieldMixin

from rest_framework.exceptions import MethodNotAllowed, NotFound, ValidationError
from rest_framework.decorators import api_view, action 
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

# from .utils import get_tokens_for_user

from dj_rest_auth.views import LoginView as dj_Login

class CustomUserLogin(dj_Login):
    def get_response_serializer(self):
        return CustomJWTSerializer

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) #Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class WalletView(APIView):
    def get(self, request, format=None):
        if not request.user.is_authenticated:
            return Response(status.HTTP_403_FORBIDDEN)
        return Response(json.dumps({
                'user' : request.user.username,
                'amount' : str(request.user.wallet.amount)
            }))

class MembershipView(generics.GenericAPIView):
    """  membership
    "http://localhost:8000/api/v1/accounts/membership/"  
    "403" --> authentication problem
    post --> create --> status_code = 302 already exist
                    --> status_code = 201 created
                    --> status_code = 400 bad input
    get  ---> 302 found
         ---> 404 not found --> output = user dosent have permission
    """ 
    permission_classes = [IsAuthenticated, ]
    serializer_class = MembershipCreateSerializer
    def post(self, request):
        if request.user.have_membership:
            return Response(MembershipSerializer(instance=request.user.membership).data, status=status.HTTP_302_FOUND)
        else:
            serializer = MembershipCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if request.user.have_membership:
                return Response(MembershipSerializer(instance=request.user.membership).data, status=status.HTTP_302_FOUND)
        return Response(json.dumps({'detail' : 'user doesnt have membership'}), status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    """
        for get your information ---> /accounts/profile/
        for see profile another user --> /accounts/<str:username>/
        for retrieve or list --> you must authenticated
        for create user --->  /accounts/register/
        get all user --> /accounts/
        block user --> /accounts/<username that you want block>/blockuser/
        unblock user --> /accounts/<username that you want block>/unblockuser/
        get all user-profile-image ---> it's create for admin to retreive all profile image to accept them --> /accounts/admin-all-profile-pic/
        accept profile image -->only admin- put : /accounts/<username>/accept-profile-pic/
        get all user bio ---> it's create for admin to retreive all user bio to accept them -->get /accounts/admin-all-profile-bio/
        accpet user bio -->only admin - put : /accounts/<username>/accept-profile-bio/
    """
    permission_classes = [UserViewSetPermission]
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action in ['count_user_post', 'count_user_podcast', 'count_user_project', 'count_user_exprience']:
            return CountSerializer
        if self.action == 'user_post':
            return PostSerializer
        elif self.action == 'user_podcast':
            return PodcastSerializer
        elif self.action == 'user_project':
            return ProjectSerializer
        elif self.action == 'user_experience':
            return ExprienceSerializer
        if self.request.user.is_anonymous:
            return UserSeenInfoSerializer
        if self.request.user.is_admin:
            return UserAllInfoSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSeenInfoSerializer

    def get_queryset(self):
        return CustomeUserModel.objects.filter(emailaddress__verified=True)
  
    @action(methods=["get"], detail=False, name="user Profile", url_path='profile')
    def profile(self, request):
        return Response(UserAllInfoSerializer(instance=request.user, context={"request": request}).data)

    @action(methods=["get"], detail=True, name="count user post", url_path='count-user-post')
    def count_user_post(self, request, username):
        instance = self.get_object()
        count = Post.objects.filter(owner=instance).count()
        return Response({'count' : count})
    
    @action(methods=["get"], detail=True, name="count user podcast", url_path='count-user-podcast')
    def count_user_podcast(self, request, username):
        instance = self.get_object()
        count = Podcast.objects.filter(owner=instance).count()
        return Response({'count' : count})
    
    @action(methods=["get"], detail=True, name="count user experience", url_path='count-user-experience')
    def count_user_experience(self, request, username):
        instance = self.get_object()
        count = SuccessfullExperience.objects.filter(owner=instance).count()
        return Response({'count' : count})
    
    @action(methods=["get"], detail=True, name="count user project", url_path='count-user-project')
    def count_user_project(self, request, username):
        instance = self.get_object()
        count = Project.objects.filter(owner=instance).count()
        return Response({'count' : count})

    @action(methods=["get"], detail=True, name="user post", url_path='user-post')
    def user_post(self, request, username):
        instance = self.get_object()
        objects_ = Post.objects.filter(owner=instance)
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response(PostSerializer(page, many=True, context={"request": request}).data)
        return Response(PostSerializer(objects_, many=True, context={"request": request}).data)

    @action(methods=["get"], detail=True, name="user podcast", url_path='user-podcast')
    def user_podcast(self, request, username):
        instance = self.get_object()
        objects_ = Podcast.objects.filter(owner=instance)
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response(PodcastSerializer(page, many=True, context={"request": request}).data)
        return Response(PodcastSerializer(objects_, many=True, context={"request": request}).data)

    @action(methods=["get"], detail=True, name="user prject", url_path='user-project')
    def user_project(self, request, username):
        instance = self.get_object()
        objects_ = Project.objects.filter(owner=instance)
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response(ProjectSerializer(page, many=True, context={"request": request}).data)
        return Response(ProjectSerializer(objects_, many=True, context={"request": request}).data)

    @action(methods=["get"], detail=True, name="user exprience", url_path='user-exprience')
    def user_exprience(self, request, username):
        instance = self.get_object()
        objects_ = SuccessfullExperience.objects.filter(owner=instance)
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response(ExprienceSerializer(page, many=True, context={"request": request}).data)
        return Response(ExprienceSerializer(objects_, many=True, context={"request": request}).data)

    @action(methods=["put"], detail=True, name="block user", url_path='blockuser')
    def blockuser(self, request, username):
        instance = self.get_object()
        instance.blacklist.add(self.request.user)
        instance.save()
        return Response(status.HTTP_200_OK)

    @action(methods=["put"], detail=True, name="block user", url_path='unblockuser')
    def unblockuser(self, request, username):
        instance = self.get_object()
        instance.blacklist.remove(self.request.user)
        instance.save()
        return Response(status.HTTP_200_OK)
    # show all user profile pic that dosent accept by admin
    @action(methods=["get"], detail=False, name="user profile pic", url_path='admin-all-profile-pic')
    def user_profile_pic(self, request):
        objects_ = self.get_queryset().filter(profile_pic__admin_check=False)
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response( UserProfileSerializer(page, many=True, context={"request": request}).data)
        serializer = UserProfileSerializer(objects_, many=True, context={"request": request})
        return Response(serializer.data)
    # show all user bio  that dosent accept by admin
    @action(methods=["get"], detail=False, name="user profile bio", url_path='admin-all-profile-bio')
    def user_profile_bio(self, request):
        objects_ = self.get_queryset().filter(profile_pic__admin_check=False)
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response( UserBioSerializer(page, many=True, context={"request": request}).data)
        serializer = UserBioSerializer(objects_, many=True, context={"request": request})
        return Response(serializer.data)
    
    @action(methods=["get"], detail=False, name="show user feedback", url_path='show-user-feedback')
    def show_user_feedback(self, request):
        objects_ =  UserFeedbackOpinion.objects.filter(receiver=self.request.user)
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response( UserFeedbackListSerializer(page, many=True, context={"request": request}).data)
        serializer = UserFeedbackListSerializer(objects_, many=True, context={"request": request})
        return Response(serializer.data)
    

    @action(methods=["post"], detail=True, name="accpet profile pic", url_path='accept-profile-pic')
    def accept_profile_pic(self, request, username):
        instance = self.get_object()
        pic = instance.profile_pic
        pic.admin_check = True
        pic.save()
        return Response(status.HTTP_200_OK)

    @action(methods=["post"], detail=True, name="accpet profile pic", url_path='accept-user-bio')
    def accept_profile_pic(self, request, username):
        instance = self.get_object()
        bio = instance.user_bio
        bio.admin_check = True
        bio.save()
        return Response(status.HTTP_200_OK)

    @action(methods=["get"], detail=False, name="number register", url_path='number-register')
    def number_register(self, request):
        queryset = self.get_queryset()
        daily =  queryset.filter(date_joined__gte=timezone.now() - timedelta(hours=24))
        weekly = queryset.filter(date_joined__gte=timezone.now() - timedelta(days=7))
        monthly = queryset.filter(date_joined__gte=timezone.now() - timedelta(days=30))
        yearly = queryset.filter(date_joined__gte=timezone.now() - timedelta(days=365))
        data = {
            'count' : queryset.count(),
            'number_in_day': daily.count(),
            'number_in_week': weekly.count(),
            'number_in_month': monthly.count(),
            'number_in_year': yearly.count(),
        }
        return Response((data))  
    @action(methods=["get"], detail=False, name="number activate user", url_path='number-active')
    def number_active(self, request):
        queryset = self.get_queryset()
        daily =  queryset.filter(last_login__gte=timezone.now() - timedelta(hours=24))
        weekly = queryset.filter(last_login__gte=timezone.now() - timedelta(days=7))
        monthly = queryset.filter(last_login__gte=timezone.now() - timedelta(days=30))
        yearly = queryset.filter(last_login__gte=timezone.now() - timedelta(days=365))
        data = {
            'count' : queryset.count(),
            'number_in_day': daily.count(),
            'number_in_week': weekly.count(),
            'number_in_month': monthly.count(),
            'number_in_year': yearly.count(),
        }
        return Response((data))



class UpdateBioView(generics.UpdateAPIView):
    """
        change profile bio --> /accounts/change-bio/
    """
    queryset = UserBio.objects.all()
    serializer_class = UpdateBioSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return UserBio.objects.get(owner=self.request.user)
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.admin_check = False
        instance.save()
        return super().put(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.admin_check = False
        instance.save()
        return super().patch(request, *args, **kwargs)    
    
class UpdateProfilePicView(generics.UpdateAPIView):
    """
        change profile Pic --> /accounts/change-profile-image/
    """
    queryset = ProfileImage.objects.all()
    serializer_class = UpdateProfilePicSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return ProfileImage.objects.get(owner=self.request.user)
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.admin_check = False
        instance.save()
        return super().put(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.admin_check = False
        instance.save()
        return super().patch(request, *args, **kwargs)    

class CustomVerifyEmail(generics.GenericAPIView):
    permission_classes = ()
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')
    serializer_class = CustomVerifyEmailSerializer

    def get(self, *args, **kwargs):
        raise MethodNotAllowed('GET')
    def post(self, *args, **kwargs):
        activation = ActivationKey.objects.get(key=self.request.data['key'])
        user_ = activation.user 
        try:
            emailaddress = user_.emailaddress_set.all()[0]
            if not emailaddress.verified:
                emailaddress.verified = True 
                emailaddress.save()
                activation.delete()
                return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except:
            activation.delete()
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class CustomUserIdApiView(generics.GenericAPIView):
    """
        create userId
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserIdSerializer
    def get(self, *args, **kwargs):
        if self.request.user.userid != None:
            return Response(UserIdSerializer(instance=self.request.user.userid).data)
        return Response(data={'detail': 'user dosent have user_id'}, status=status.HTTP_404_NOT_FOUND)
    def post(self, *args, **kwargs):
        serializer_ = UserIdSerializer(data=self.request.data)
        serializer_.is_valid(raise_exception=True)
        # if userId is exist get userId and delete
        if not self.request.user.userid == None:
            userid_ = self.request.user.userid 
            userid_.delete()
        obj = serializer_.save()
        user_ = self.request.user
        # if admin change he's userid it's admin_check=True
        if user_.is_admin:
            obj.admin_check = True 
            obj.save()
        user_.userid = obj
        user_.save()
        return Response(status=status.HTTP_200_OK)

class CheckUserIdApiView(generics.GenericAPIView):
    """
        status 200 ok
        status 302 found -> it's duplicate
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserIdSerializer
    def post(self, *args, **kwargs):
        key = self.request.data['userid']
        if UserId.objects.filter(userid=key).count() > 0:
            return Response(data={'detail': "it's duplicated"}, status=status.HTTP_302_FOUND)
        return Response(data={'detail': "it's ok"}, status=status.HTTP_200_OK)


class SupportMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [SupportMessagePermission]
    serializer_class = SupportMessageSerializer
    def get_queryset(self):
        return SupportMessage.objects.filter(Q(owner=self.request.user) | Q(user_receive=self.request.user)) 
    
    @action(methods=["get"], detail=False, name="user send message", url_path='send')
    def user_send(self, request):
        objects_ = self.get_queryset().filter(Q(owner=self.request.user))
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response( SupportMessageSerializer(page, many=True, context={"request": request}).data)
        serializer = SupportMessageSerializer(objects_, many=True, context={"request": request})
        return Response(serializer.data)
    
    @action(methods=["get"], detail=False, name="user send message", url_path='receive')
    def user_receive(self, request):
        objects_ = self.get_queryset().filter(Q(user_receive=self.request.user))
        page = self.paginate_queryset(objects_)
        if page is not None:
            return self.get_paginated_response( SupportMessageSerializer(page, many=True, context={"request": request}).data)
        serializer = SupportMessageSerializer(objects_, many=True, context={"request": request})
        return Response(serializer.data)

class UserFeedbackCreateApiView(generics.CreateAPIView):
    serializer_class = UserFeedbackSerializer
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

# UserId.objects.create(userid)

# class RegistrationView(generics.GenericAPIView):

#     serializer_class = RegistrationSerializer
#     # renderer_classes = (UserRenderer,)

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         user = CustomeUserModel.objects.get(email=user_data['email'])
#         token = RefreshToken.for_user(user).access_token
#         current_site = get_current_site(request).domain
#         relativeLink = reverse('users_api:email-verify')
#         absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#         send_verification_email(name=user.username, email=user.email, verify_link=absurl)
#         return Response(user_data, status=status.HTTP_201_CREATED)



# class VerifyEmail(views.APIView):
#     def get(self, request):
#         pass
# # class RegistrationView(APIView):
# #     def post(self, request):
# #         serializer = RegistrationSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

