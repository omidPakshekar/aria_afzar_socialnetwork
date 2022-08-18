from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView
# from .utils import get_tokens_for_user
from .serializers import MembershipCreateSerializer, MembershipSerializer, PasswordChangeSerializer, RegistrationSerializer

import json

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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



