from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import generics, status, views, permissions, viewsets
from chat.models import Chat, Contact
# from chat.views import get_user_contact
from .serializers import ChatSerializer, ContactSerializer
from rest_framework.response import Response

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



# update and partial update and add delete for owner and admin
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )
    contact = None 

    def create(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, created = Contact.objects.get(owner=self.request.user, )
        print('*&*&&*&=', obj)
        print('created=', created)
        if created:
            return Response({"detail": "fff"})
        self.contact = serializer.save(owner=self.request.user)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(participants=self.contact)









