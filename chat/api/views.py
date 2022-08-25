from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import generics, status, views, permissions, viewsets
from chat.models import Chat, Contact
# from chat.views import get_user_contact
from .serializers import ChatSerializer

User = get_user_model()


# class ChatListView(ListAPIView):
#     serializer_class = ChatSerializer
#     permission_classes = (permissions.AllowAny, )

#     def get_queryset(self):
#         queryset = Chat.objects.all()
#         username = self.request.query_params.get('username', None)
#         if username is not None:
#             contact = get_user_contact(username)
#             queryset = contact.chats.all()
#         return queryset



class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )










