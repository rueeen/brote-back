"""Admin registrations for evaluaciones."""
from django.contrib import admin

from .models import Evaluacion


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = (
        "uuid_publico",
        "rubro",
        "ciudad",
        "estado",
        "creado_en",
        "actualizado_en",
    )
    list_filter = ("rubro", "estado", "creado_en")
    search_fields = ("uuid_publico", "ciudad", "publico", "descripcion")
    readonly_fields = ("uuid_publico", "creado_en", "actualizado_en")
