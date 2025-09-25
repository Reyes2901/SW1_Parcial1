from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Project
from .serializers import ProjectSerializer, CollaboratorSerializer

User = get_user_model()


class IsOwnerOrCollaborator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user in obj.collaborators.all()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCollaborator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user) | Project.objects.filter(collaborators=self.request.user)

    @action(detail=True, methods=['post'], url_path='collaborators', permission_classes=[permissions.IsAuthenticated])
    def add_collaborator(self, request, pk=None):
        project = self.get_object()

        if project.owner != request.user:
            return Response({"detail": "Solo el propietario puede agregar colaboradores."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CollaboratorSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)

                if user == request.user:
                    return Response({"detail": "No puedes agregarte a ti mismo como colaborador."}, status=400)

                if user in project.collaborators.all():
                    return Response({"detail": "El usuario ya es colaborador."}, status=400)

                project.collaborators.add(user)
                return Response({"detail": f"Colaborador '{username}' agregado exitosamente."})
            except User.DoesNotExist:
                return Response({"detail": "Usuario no encontrado."}, status=404)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['delete'], url_path='collaborators/(?P<username>[^/.]+)', permission_classes=[permissions.IsAuthenticated])
    def remove_collaborator(self, request, pk=None, username=None):
        project = self.get_object()

        if project.owner != request.user:
            return Response({"detail": "Solo el propietario puede eliminar colaboradores."}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(username=username)

            if user == project.owner:
                return Response({"detail": "No puedes eliminar al propietario del proyecto."}, status=400)

            if user not in project.collaborators.all():
                return Response({"detail": "Este usuario no es colaborador."}, status=400)

            project.collaborators.remove(user)
            return Response({"detail": f"Colaborador '{username}' eliminado correctamente."})
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=404)
