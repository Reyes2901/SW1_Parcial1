# diagrams/serializers.py
from rest_framework import serializers
from .models import Diagram

class DiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagram
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


# diagrams/serializers.py (continúa abajo del anterior)

class AttributeSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    visibility = serializers.ChoiceField(choices=["public", "private", "protected"])

class MethodSerializer(serializers.Serializer):
    name = serializers.CharField()
    return_type = serializers.CharField()
    visibility = serializers.ChoiceField(choices=["public", "private", "protected"])

class ClassSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    attributes = AttributeSerializer(many=True)
    methods = MethodSerializer(many=True)
    position = serializers.DictField()

class RelationSerializer(serializers.Serializer):
    from_ = serializers.CharField(source="from")
    to = serializers.CharField()
    type = serializers.ChoiceField(choices=["hasOne", "hasMany", "inherits"])

class DiagramContentSerializer(serializers.Serializer):
    diagram_name = serializers.CharField()
    classes = ClassSerializer(many=True)
    relations = RelationSerializer(many=True, required=False)
    updated_at = serializers.DateTimeField()
