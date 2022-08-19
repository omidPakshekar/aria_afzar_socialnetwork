from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action 
from rest_framework.response import Response

from .serializers import ExprienceCreateSerializer, ExprienceSerializer


from ..models import SuccessfullExperience




class ExprienceViewSet(viewsets.ModelViewSet):
    queryset = SuccessfullExperience.objects.all()
    permission_classes = [IsAuthenticated]
    # serializer_class = ExprienceCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ExprienceCreateSerializer
        return ExprienceSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    








