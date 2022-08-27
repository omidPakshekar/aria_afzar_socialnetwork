import json
from .models import *

from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer


User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    async def websocket_connect(self, event):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat = await self.get_chat()
        self.chat_room_id = f"chat_{self.chat_id}"

        if self.chat:
            if self.user in self.chat.participants.all():
                await self.channel_layer.group_add(
                    self.chat_room_id,
                    self.channel_name
                )
                await self.send({
                    'type': 'websocket.accept'
                })
        else:
            await self.send({
                'type': 'websocket.close'
            })


    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.chat_room_id,
            self.channel_name
        )
        raise StopConsumer()


    async def websocket_receive(self, event):
        text_data = event.get('text', None)
        bytes_data = event.get('bytes', None)

        if text_data:
            text_data_json = json.loads(text_data)
            text = text_data_json['text']

            await self.create_message(text)
            
            await self.channel_layer.group_send(
                self.chat_room_id,
                {
                    'type': 'chat_message',
                    'message': json.dumps({'type':"msg", 'sender':self.user.username, 'text':text}),
                    'sender_channel_name': self.channel_name
                }
            )

    async def chat_message(self, event):
        message = event['message']
        
        if self.channel_name != event['sender_channel_name']:
            await self.send({
                'type': 'websocket.send',
                'text': message
            })


    @database_sync_to_async
    def get_chat(self):
        try:
            chat = GroupChat.objects.get(unique_code=self.chat_id)
            return chat
        except GroupChat.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, text):
        message_ = Message.objects.create( owner=self.user.id, message_text=text)
        self.chat.messages.add(message_)

    def fetch_messages(self, data):
        messages = self.chat.messages.all()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

