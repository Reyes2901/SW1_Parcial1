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

class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
