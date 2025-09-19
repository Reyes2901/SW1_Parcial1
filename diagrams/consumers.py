# /backend/diagrams/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from diagrams.models import Diagram
from django.contrib.auth import get_user_model

User = get_user_model()

class DiagramConsumer(AsyncWebsocketConsumer):
    active_locks = {}  # Bloqueos de nodos por usuario

    async def connect(self):
        self.diagram_id = self.scope['url_route']['kwargs']['diagram_id']
        self.group_name = f'diagram_{self.diagram_id}'
        user = self.scope["user"]
        diagram = await self.get_diagram()

        if user.is_authenticated and await self.user_has_access(diagram, user):
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

            # Notificar conexión
            await self.channel_layer.group_send(
                self.group_name,
                {"type": "user_joined", "user": user.username}
            )
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "user_left", "user": self.scope["user"].username}
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get("type")

        # 🔁 Guardar contenido en cada cambio relevante
        if event_type in ["add_class", "update_class", "delete_class"]:
            await self.save_diagram_content(data.get("content"))

        # 🔒 Gestión de bloqueo de nodos
        if event_type == "lock_node":
            node_id = data.get("node_id")
            user = self.scope["user"].username
            if node_id not in self.active_locks:
                self.active_locks[node_id] = user
                data["status"] = "locked"
            else:
                data["status"] = "already_locked"
                data["locked_by"] = self.active_locks[node_id]

        elif event_type == "unlock_node":
            node_id = data.get("node_id")
            user = self.scope["user"].username
            if self.active_locks.get(node_id) == user:
                del self.active_locks[node_id]
                data["status"] = "unlocked"

        # 🔊 Reenviar evento a todos los usuarios conectados
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_event",
                "payload": data
            }
        )

    async def broadcast_event(self, event):
        await self.send(text_data=json.dumps(event["payload"]))

    async def user_joined(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_joined",
            "user": event["user"]
        }))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_left",
            "user": event["user"]
        }))

    @database_sync_to_async
    def get_diagram(self):
        try:
            return Diagram.objects.select_related("project").get(pk=self.diagram_id)
        except Diagram.DoesNotExist:
            return None

    @database_sync_to_async
    def user_has_access(self, diagram, user):
        return (
            diagram.created_by == user or
            user in diagram.project.collaborators.all()
        )

    @database_sync_to_async
    def save_diagram_content(self, new_content):
        from .models import DiagramVersion  # Evitar import circular

        diagram = Diagram.objects.get(pk=self.diagram_id)

        # Guardar versión anterior
        DiagramVersion.objects.create(
            diagram=diagram,
            content=diagram.content,
            created_by=self.scope["user"]
        )

        # Guardar nuevo contenido
        diagram.content = new_content
        diagram.save()
        return
        # Limpieza del directorio temporal si es necesario
        