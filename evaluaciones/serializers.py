"""Serializers for evaluation input and API responses."""

from rest_framework import serializers


RUBRO_CHOICES = [
    'tecnologia',
    'gastronomia',
    'retail',
    'salud',
    'educacion',
    'servicios',
    'sustentabilidad',
    'otro',
]


class EvaluacionInputSerializer(serializers.Serializer):
    """Validate the public form used to request a business evaluation."""

    rubro = serializers.ChoiceField(choices=RUBRO_CHOICES)
    publico = serializers.CharField(min_length=2, max_length=200)
    descripcion = serializers.CharField(
        min_length=30,
        max_length=2000,
        error_messages={
            'blank': 'La descripción no puede estar vacía.',
            'required': 'La descripción es obligatoria.',
            'min_length': 'La descripción debe tener al menos 30 caracteres.',
            'max_length': 'La descripción no puede superar los 2000 caracteres.',
        },
    )
    ciudad = serializers.CharField(min_length=2, max_length=100)
    presupuesto_disponible = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
    )

    def validate_descripcion(self, value):
        """Require a meaningful description, not just enough characters."""
        palabras = value.split()
        if len(palabras) < 5:
            raise serializers.ValidationError(
                'La descripción debe tener al menos 5 palabras.'
            )
        return value


class EvaluacionOutputSerializer(serializers.Serializer):
    """Serialize a full evaluation response for the frontend."""

    rubro = serializers.ChoiceField(choices=RUBRO_CHOICES)
    publico = serializers.CharField(max_length=200)
    descripcion = serializers.CharField()
    ciudad = serializers.CharField(max_length=100)
    presupuesto_disponible = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
    )
    uuid = serializers.UUIDField(read_only=True)
    estado = serializers.CharField(read_only=True)
    creado_en = serializers.DateTimeField(read_only=True)
    resultado = serializers.JSONField(read_only=True)


class EvaluacionListSerializer(serializers.Serializer):
    """Serialize evaluations for list views without exposing the full JSON."""

    uuid = serializers.UUIDField(read_only=True)
    rubro = serializers.ChoiceField(choices=RUBRO_CHOICES)
    ciudad = serializers.CharField(max_length=100)
    puntaje_global = serializers.SerializerMethodField()
    estado = serializers.CharField(read_only=True)
    creado_en = serializers.DateTimeField(read_only=True)

    def get_puntaje_global(self, obj):
        if isinstance(obj, dict):
            resultado = obj.get('resultado')
        else:
            resultado = getattr(obj, 'resultado', None)

        if isinstance(resultado, dict):
            return resultado.get('puntaje_global')
        return None
