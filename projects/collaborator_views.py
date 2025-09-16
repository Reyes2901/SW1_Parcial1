from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Project
from django.contrib.auth import get_user_model
from .serializers import CollaboratorSerializer
from .permissions import IsProjectOwnerOrCollaborator

User = get_user_model()

class CollaboratorListCreateView(generics.ListCreateAPIView):
    serializer_class = CollaboratorSerializer
    permission_classes = [IsAuthenticated, IsProjectOwnerOrCollaborator]

    def get_queryset(self):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        self.check_object_permissions(self.request, project)
        return project.collaborators.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        # Solo el owner puede agregar
        if request.user != project.owner:
            return Response({'detail': 'Solo el owner puede agregar colaboradores.'}, status=403)
        username = request.data.get('username')
        # Seguridad: Verifica permisos
        if not username:
            return Response({'detail': 'Debes proporcionar un username.'}, status=400)
        # Verifica si el usuario existe
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': f'El usuario "{username}" no existe.'}, status=404)
        # Evitar que el owner se agregue a sí mismo
        if user == project.owner:
            return Response({'detail': 'El owner ya es parte del proyecto.'}, status=400)
        # Evitar agregar colaboradores duplicados
        if user in project.collaborators.all():
            return Response({'detail': f'El usuario "{username}" ya es colaborador.'}, status=400)
        
        project.collaborators.add(user)
        return Response({'detail': f'El usuario "{username}" ha sido agregado como colaborador.'}, status=201)

class CollaboratorDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        self.check_object_permissions(self.request, project)
        #Solo el owner puede eliminar colaboradores
        #Seguridad: Verifica permisos
        if request.user != project.owner:
            return Response({'detail': 'Solo el owner puede eliminar colaboradores.'}, status=403)
        #Evitar que el owner se elimine a sí mismo
        if user == project.owner:
            return Response({'detail': 'No puedes eliminar al owner del proyecto.'}, status=400)
        
        if user not in project.collaborators.all():
            return Response({'detail': 'El usuario no es colaborador del proyecto.'}, status=404)
        project.collaborators.remove(user)
        return Response({'detail': f'{user.username} eliminado del proyecto.'}, status=204)
