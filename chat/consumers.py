from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from channels.consumer import SyncConsumer, AsyncConsumer

import json
from .models import *

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    async def fetch_messages(self, data):
        messages = self.chat.messages.all()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    async def new_message(self, data):
        await self.create_message(data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return await self.send_chat_message(content)

    async def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    async def message_to_json(self, message):
        return {
            'id': message.id,
            'owner': message.owner.username,
            'message_text': message.message_text,
            'timestamp': str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    async def connect(self):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat = await self.get_chat()
        self.chat_room_id = f"chat_{self.chat_id}"
        print('ffffffff')
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
                self.close(403)
        else:
            await self.send({
                'type': 'websocket.close'
            })

    async def disconnect(self, close_code):
        await (self.channel_layer.group_discard)(
            self.chat_room_id,
            self.channel_name
        )
        raise StopConsumer()


    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.commands[data['command']](self, data)

    async def send_chat_message(self, message):
        (self.channel_layer.group_send)(
            self.chat_room_id,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

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
