from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    collaborators = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'collaborators', 'start_date', 'created_at']
User = get_user_model()

class CollaboratorSerializer(serializers.Serializer):
    #Serializar por ModelSerializer: no esta creado un modelo específico para colaboradores
    #Solo usando el username para agregar/eliminar colaboradores
    
    username = serializers.CharField()

    def validate_username(self, value):
        User = get_user_model()
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("El usuario no existe.")
        return value
