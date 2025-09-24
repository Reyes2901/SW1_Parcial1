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

class DiagramListCreateAPI(generics.ListCreateAPIView):
    serializer_class = DiagramSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Diagram.objects.filter(
            project__collaborators=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DiagramDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diagram.objects.all()
    serializer_class = DiagramSerializer
    permission_classes = [permissions.IsAuthenticated, IsCollaboratorOrReadOnly]

    def get_queryset(self):
        return Diagram.objects.filter(project__collaborators=self.request.user)



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
                return Response({"error": "El diagrama ha sido modificado por otro usuario."}, status=409)

            diagram.content = serializer.validated_data
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
