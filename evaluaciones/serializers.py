from rest_framework import serializers

class EvaluacionInputSerializer(serializers.Serializer):
    rubro       = serializers.ChoiceField(choices=[
        'tecnologia','gastronomia','retail','salud',
        'educacion','servicios','sustentabilidad','otro'
    ])
    publico     = serializers.CharField(max_length=200)
    descripcion = serializers.CharField(min_length=30, max_length=2000)
    ciudad      = serializers.CharField(max_length=100)
    presupuesto_disponible = serializers.CharField(
        max_length=50, required=False, allow_blank=True
    )
