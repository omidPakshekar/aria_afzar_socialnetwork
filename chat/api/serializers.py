from rest_framework import serializers

from chat.models import *
# from .views import get_last_10_messages, get_user_contact, get_current_chat



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["friends"]




# class ContactSerializer(serializers.StringRelatedField):
#     def to_internal_value(self, value):
#         return value

class ChatContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('id', 'contact', )
        read_only = ('id')


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('id', 'messages', )
        read_only = ('id')

    # def create(self, validated_data):
    #     print(validated_data)
    #     # participants = validated_data.pop('participants')
    #     print('fffffffff', validated_data)
    #     chat = Chat()
    #     chat.save()
    #     for username in participants:
    #         contact = get_user_contact(username)
    #         chat.participants.add(contact)
    #     chat.save()
        # return chat


# do in python shell to see how to serialize data

# from chat.models import Chat
# from chat.api.serializers import ChatSerializer
# chat = Chat.objects.get(id=1)
# s = ChatSerializer(instance=chat)
# s
# s.data
