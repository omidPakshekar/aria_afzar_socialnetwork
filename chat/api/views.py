from django.contrib.auth import get_user_model
from django.db.models import Q, Count

from rest_framework import permissions
from rest_framework import generics, status, views, permissions, viewsets
from chat.models import Chat, Contact
# from chat.views import get_user_contact
from .serializers import ChatSerializer, ContactSerializer
from rest_framework.response import Response


User = get_user_model()


# group1 = Contact.objects.annotate(
#     nusers=Count('friends'),
#     nusers_match=Count('friends', filter=Q(friends__in=cs))
# ).filter(
#     nusers=len(cs),
#     nusers_match=len(cs)
# )

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


#  g = Contact.objects.annotate(nusers=Count('friends'), nuser_match=Count('friends', filter=Q(friends__in=c['friends'])))
# update and partial update and add delete for owner and admin
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, )
    contact = None 

    def create(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print('**********\n', serializer.validated_data['friends'], '************\n')
        cs = serializer.validated_data['friends']
        contact_ = Contact.objects.annotate(
            nusers=Count('friends'),
            nusers_match=Count('friends', filter=Q(friends__in=cs))
        ).filter(
            nusers=len(cs),
            nusers_match=len(cs)
        )
        if contact_.count() == 0:
            contact = serializer.save(owner=self.request.user)
            chat_ = Chat.objects.create(participants=contact)
            print('unique_code=', chat_.id, chat_.unique_code)
            return Response(data = {'chat_id': chat_.unique_code}, status=status.HTTP_201_CREATED)
        return Response(data = {'chat_id': contact_[0].chats.all()[0].unique_code}, status=status.HTTP_200_OK)
        
    #     

    
        # obj, created = Contact.objects.get(owner=self.request.user, )
    #     print('*&*&&*&=', obj)
    #     print('created=', created)
    #     if created:
    #         return Response({"detail": "fff"})
    #     self.contact = serializer.save(owner=self.request.user)
        # return super().create(request, *args, **kwargs)

    # def perform_create(self, serializer):
    #     serializer.save(participants=self.contact)







