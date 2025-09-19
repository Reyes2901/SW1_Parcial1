from rest_framework import generics, permissions
from .models import Diagram
from .serializers import DiagramSerializer

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
