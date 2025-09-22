from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DiagramConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'diagram_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'diagram_message',
                'message': text_data,
            }
        )

    async def diagram_message(self, event):
        await self.send(text_data=event['message'])
# from channels.generic.websocket import AsyncWebsocketConsumer