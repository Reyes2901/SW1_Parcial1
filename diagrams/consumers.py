from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Diagram
import json

class DiagramConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #self.room_name = self.scope['url_route']['kwargs']['room_name']
        #self.room_group_name = f'diagram_{self.room_name}'
        self.diagram_id = self.scope['url_route']['kwargs']['diagram_id']
        self.room_group_name = f'diagram_{self.diagram_id}'

        self.user = self.scope["user"]

        if not await self.user_can_access():
            await self.close()
            return
        
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
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))
            return
        #Reenviar el mensaje a todos los miembros del grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'diagram_message',
                'user': self.user.username,
                'message': text_data,
            }
        )

    async def diagram_message(self, event):
        await self.send(text_data=json.dumps({
            "user": event['user'],
            "message": event['message']
        }))
    @database_sync_to_async
    def user_can_access(self):
        if isinstance(self.user, AnonymousUser):
            return False
        try:
            diagram = Diagram.objects.get(id=self.diagram_id)
        except Diagram.DoesNotExist:
            return False

        if self.user == diagram.created_by or self.user in diagram.project.collaborators.all():
            return True
        return False
# from channels.generic.websocket import AsyncWebsocketConsumer