from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import sync_to_async

import json
from .models import *

User = get_user_model()


class ChatConsumer(AsyncConsumer):

    async def fetch_messages(self, data):
        messages = await self.get_all_message()
        content = {
            'command': 'messages',
            'messages': await self.messages_to_json(messages)
        }
        await self.send_message(content)

    async def new_message(self, data):
        message_ = await self.create_message(data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message_)
        }
        return await self.send_chat_message(content)

    
    async def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(await self.message_to_json(message))
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

    async def websocket_connect(self, event):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat = await self.get_chat()
        self.chat_room_id = f"chat_{self.chat_id}"
        if self.chat:
            
            if await self.check_auth():
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

    async def websocket_disconnect(self, close_code):
        await (self.channel_layer.group_discard)(
            self.chat_room_id,
            self.channel_name
        )
        raise StopConsumer()


    async def websocket_receive(self, event):
        text_data = event.get('text', None)
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

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def get_chat(self):
        try:
            chat = Chat.objects.get(unique_code=self.chat_id)
            self.participants = chat.participants
            return chat
        except Chat.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, text):
        message_ = Message.objects.create( owner=self.user, message_text=text)
        self.chat.messages.add(message_)
        return message_
    
    @sync_to_async
    def check_auth(self):
        print(self.user)
        return self.user in self.participants.friends.all() or self.user == self.participants.owner
    @sync_to_async
    def get_all_message(self):
        return self.chat.messages.all()
