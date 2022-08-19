from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action 
from rest_framework.response import Response

from .serializers import ExprienceCreateSerializer


from ..models import SuccessfullExperience




class ExprienceViewSet(viewsets.ModelViewSet):
    queryset = SuccessfullExperience
    permission_classes = [IsAuthenticated]
    serializer_class = ExprienceCreateSerializer

    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    








