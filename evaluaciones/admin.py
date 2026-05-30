"""Admin registrations for evaluaciones."""

from django.contrib import admin

from .models import Evaluacion


@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    """Admin configuration for reviewing idea evaluations."""

    list_display = ("rubro", "ciudad", "estado", "puntaje_global", "creado_en")
    list_filter = ("estado", "rubro", "creado_en")
    search_fields = ("ciudad", "publico", "descripcion", "uuid")
    readonly_fields = ("uuid", "creado_en", "ip_origen", "resultado")
    ordering = ("-creado_en",)
    date_hierarchy = "creado_en"

    @admin.display(description="Puntaje global")
    def puntaje_global(self, obj):
        """Return the global score from the AI result JSON, when available."""
        if not isinstance(obj.resultado, dict):
            return "—"

        return obj.resultado.get("puntaje_global", "—")
