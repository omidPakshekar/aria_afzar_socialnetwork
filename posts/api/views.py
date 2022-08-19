from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action 
from rest_framework.response import Response
from rest_framework import status

from posts.api.permissions import PostPermission

from .serializers import ExprienceCreateSerializer, ExprienceSerializer
from ..models import SuccessfullExperience




class ExprienceViewSet(viewsets.ModelViewSet):
    queryset = SuccessfullExperience.objects.all()
    permission_classes = [PostPermission]
    # serializer_class = ExprienceCreateSerializer

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
        instance.user_liked.add(self.request.user)
        return Response(status.HTTP_200_OK)
    
    @action(methods=["put"], detail=True, name="user saved", url_path='save')
    def add_user_saved(self, request, pk):
        instance = self.get_object()
        instance.user_saved.add(self.request.user)
        return Response(status.HTTP_200_OK)






