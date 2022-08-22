import json, jwt, os

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
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions, viewsets
from rest_framework_simplejwt.tokens import RefreshToken

# from .utils import get_tokens_for_user

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
        print(request.user)
        return Response(json.dumps({
                'user' : request.user.username,
                'amount' : str(request.user.wallet.amount)
            }))

class MembershipView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            if request.user.membership:
                return Response(MembershipSerializer(instance=request.user.membership).data, status=status.HTTP_302_FOUND)
        except:
            serializer = MembershipCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            if request.user.membership:
                return Response(MembershipSerializer(instance=request.user.membership).data, status=status.HTTP_302_FOUND)
        except:
            return Response(json.dumps({'detail' : 'user doesnt have membership'}), status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [UserViewSetPermission]
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserSeenInfoSerializer
        return UserAllInfoSerializer
    def get_queryset(self):
        return CustomeUserModel.objects.filter(emailaddress__verified=True)
  
    # @action(methods=["put"], detail=True, name="user saved", url_path='admin-accept')
    # def admin_accept(self, request, pk):

 
    # @action(methods=["put"], detail=True, name="user saved", url_path='admin-accept')
    # def admin_accept(self, request, pk):
    #     if request.user.is_admin:
    #         return Response(
    #                         json.dumps({'detail' : 'only admin can do'}),
    #                         status=status.HTTP_403_FORBIDDEN
    #                     )
    #     instance = self.get_object()






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

