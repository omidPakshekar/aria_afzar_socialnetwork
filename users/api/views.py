import json, jwt, os
from urllib import request

from .serializers import UserAllInfoSerializer, UserSeenInfoSerializer
from users.api.permissions import UserViewSetPermission
from .serializers import *
from ..email import send_verification_email  

from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout

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
       for retrieve or list --> you must authenticated
       for create user --->  \accounts\register 
    """
    permission_classes = [UserViewSetPermission]
    lookup_field = 'username'

    def get_serializer_class(self):
        try:
            if self.request.user.is_admin:
                return UserAllInfoSerializer
        except: pass
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSeenInfoSerializer

    def get_queryset(self):
        return CustomeUserModel.objects.filter(emailaddress__verified=True)
  
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
    @action(methods=["get"], detail=False, name="user profile pic", url_path='user-profile-pic')
    def user_profile_pic(self, request):
        objects_ = self.get_queryset().filter(profile_pic__admin_check=False)
        page = self.paginate_queryset(objects_)
        if page is not None:
            serializer = UserProfileSerializer(page, many=True, context={"request": request})
        serializer = UserProfileSerializer(objects_, many=True, context={"request": request})
        return Response(serializer.data)
    # show all user bio  that dosent accept by admin
    @action(methods=["get"], detail=False, name="user profile bio", url_path='user-profile-bio')
    def user_profile_bio(self, request):
        objects_ = self.get_queryset().filter(profile_pic__admin_check=False)
        page = self.paginate_queryset(objects_)
        if page is not None:
            serializer = UserBioSerializer(page, many=True, context={"request": request})
        serializer = UserBioSerializer(objects_, many=True, context={"request": request})
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

class UserBioView(generics.UpdateAPIView):
    queryset = UserBio.objects.all()
    serializer_class = UpdateBioSerializer
    def get_object(self):
        return UserBio.objects.get(owner=self.request.user)
    

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

