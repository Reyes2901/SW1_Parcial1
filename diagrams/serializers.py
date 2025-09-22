from rest_framework import serializers
from .models import Diagram
#        fields = ['id', 'name', 'project', 'created_by', 'content', 'created_at', 'updated_at']
#        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
class DiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagram
        #En vez de listar todos los campos, usamos '__all__' para incluir todos los campos del modelo
        fields = '__all__'
