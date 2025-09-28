from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from .models import Project
from .serializers import ProjectSerializer, CollaboratorSerializer

User = get_user_model()


class IsOwnerOrCollaborator(permissions.BasePermission):
    """Permite acceso solo al propietario o colaboradores del proyecto."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user in obj.collaborators.all()


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API para CRUD de proyectos y gestión de colaboradores.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCollaborator]

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(collaborators=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='collaborators',
            permission_classes=[permissions.IsAuthenticated])
    def add_collaborator(self, request, pk=None):
        """Agrega un colaborador al proyecto (solo propietario)."""
        project = self.get_object()

        if project.owner != request.user:
            return Response(
                {"detail": "Solo el propietario puede agregar colaboradores."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CollaboratorSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)

                if user == request.user:
                    return Response(
                        {"detail": "No puedes agregarte a ti mismo como colaborador."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if user in project.collaborators.all():
                    return Response(
                        {"detail": "El usuario ya es colaborador."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                project.collaborators.add(user)
                return Response(
                    {"detail": f"Colaborador '{username}' agregado exitosamente."},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response({"detail": "Usuario no encontrado."},
                                status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'],
        url_path='collaborators/(?P<user_id>\d+)')
    def remove_collaborator(self, request, pk=None, user_id=None):
        project = self.get_object()

        if project.owner != request.user:
            return Response({"detail": "Solo el propietario puede eliminar colaboradores."}, status=403)

        try:
            user = User.objects.get(pk=user_id)
            if user == project.owner:
                return Response({"detail": "No puedes eliminar al propietario."}, status=400)
            if user not in project.collaborators.all():
                return Response({"detail": "Este usuario no es colaborador."}, status=400)

            project.collaborators.remove(user)
            return Response({"detail": f"Colaborador '{user.username}' eliminado correctamente."})
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=404)

    # Otras vistas basadas en clases (CBV) para la interfaz web
