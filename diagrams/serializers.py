# diagrams/serializers.py
from rest_framework import serializers
from .models import Diagram


# ----------------------------
# Serializer principal de Diagram (CRUD básico)
# ----------------------------
class DiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagram
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Asignar automáticamente el creador
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


# ----------------------------
# Serializers para contenido de diagramas
# ----------------------------
class AttributeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=255)
    visibility = serializers.ChoiceField(choices=["public", "private", "protected"])


class MethodSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    return_type = serializers.CharField(max_length=255)
    visibility = serializers.ChoiceField(choices=["public", "private", "protected"])


class ClassSerializer(serializers.Serializer):
    id = serializers.CharField()  # Puede ser UUID o string generado en frontend
    name = serializers.CharField(max_length=255)
    attributes = AttributeSerializer(many=True)
    methods = MethodSerializer(many=True)
    position = serializers.DictField()  # {x: 100, y: 200}


class RelationSerializer(serializers.Serializer):
    from_ = serializers.CharField(source="from")  # from es palabra reservada en Python
    to = serializers.CharField()
    type = serializers.ChoiceField(choices=["hasOne", "hasMany", "inherits"])


class DiagramContentSerializer(serializers.Serializer):
    diagram_name = serializers.CharField(max_length=255)
    classes = ClassSerializer(many=True)
    relations = RelationSerializer(many=True, required=False)
    updated_at = serializers.DateTimeField(required=False)

    def validate_classes(self, value):
        # Validación básica: ids de clases únicos
        class_ids = [cls['id'] for cls in value]
        if len(class_ids) != len(set(class_ids)):
            raise serializers.ValidationError("Los IDs de las clases deben ser únicos.")
        return value

    def validate(self, data):
        # Validación opcional de relaciones
        class_ids = {cls['id'] for cls in data.get('classes', [])}
        for rel in data.get('relations', []):
            if rel['from'] not in class_ids or rel['to'] not in class_ids:
                raise serializers.ValidationError(
                    "Las relaciones deben referenciar clases existentes."
                )
        return data
