from rest_framework import generics, permissions
from .models import Diagram
from .serializers import DiagramSerializer
from django.utils.dateparse import parse_datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DiagramContentSerializer

class IsCollaboratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.created_by or
            request.user in obj.project.collaborators.all()
        )

from django.db.models import Q

class DiagramListCreateAPI(generics.ListCreateAPIView):
    serializer_class = DiagramSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get("project")
        qs = Diagram.objects.all()
        if project_id:
            qs = qs.filter(project_id=project_id)
        
        # Filtrar por usuario como owner o colaborador
        qs = qs.filter(
            Q(project__owner=self.request.user) |
            Q(project__collaborators=self.request.user)
        )
        return qs.distinct()

class DiagramDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiagramSerializer
    permission_classes = [permissions.IsAuthenticated, IsCollaboratorOrReadOnly]

    def get_queryset(self):
        qs = Diagram.objects.filter(
            Q(project__owner=self.request.user) |
            Q(project__collaborators=self.request.user)
        )
        return qs.distinct()

# Actualizar solo el contenido JSON del diagrama
# Actualizar solo el contenido JSON del diagrama
class DiagramContentUpdateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        try:
            diagram = Diagram.objects.get(pk=pk)
        except Diagram.DoesNotExist:
            return Response({"error": "Diagrama no encontrado"}, status=404)

        # Solo colaboradores o creador
        if (
            request.user != diagram.created_by and
            request.user not in diagram.project.collaborators.all()
        ):
            return Response({"error": "No tienes permiso para modificar este diagrama"}, status=403)

        serializer = DiagramContentSerializer(data=request.data)
        if serializer.is_valid():
            # Control de versiones (conflictos)
            incoming_time = parse_datetime(request.data.get("updated_at"))
            if incoming_time and incoming_time < diagram.updated_at:
                return Response(
                    {"error": "El diagrama ha sido modificado por otro usuario."},
                    status=409
                )

            # ⚡️ Guardar solo el contenido serializable
            content = serializer.validated_data.get("content", {})
            diagram.content = content

            # ⚡️ Guardar timestamp en el campo real del modelo (no dentro del JSON)
            if incoming_time:
                diagram.updated_at = incoming_time

            diagram.save()
            return Response({"message": "Contenido del diagrama actualizado"}, status=200)

        return Response(serializer.errors, status=400)

# Obtener solo el contenido JSON del diagrama
class DiagramContentReadAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            diagram = Diagram.objects.get(pk=pk)
        except Diagram.DoesNotExist:
            return Response({"error": "Diagrama no encontrado"}, status=404)

        if (
            request.user != diagram.created_by and
            request.user not in diagram.project.collaborators.all()
        ):
            return Response({"error": "No tienes permiso para ver este diagrama"}, status=403)

        return Response(diagram.content, status=200)
