import uuid

from django.core.validators import MinLengthValidator
from django.db import models


class Evaluacion(models.Model):
    """Evaluación de una idea de negocio enviada desde el formulario multi-paso."""

    class Rubro(models.TextChoices):
        TECNOLOGIA = "tecnologia", "Tecnología"
        GASTRONOMIA = "gastronomia", "Gastronomía"
        RETAIL = "retail", "Retail"
        SALUD = "salud", "Salud"
        EDUCACION = "educacion", "Educación"
        SERVICIOS = "servicios", "Servicios"
        SUSTENTABILIDAD = "sustentabilidad", "Sustentabilidad"
        OTRO = "otro", "Otro"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        PROCESANDO = "procesando", "Procesando"
        LISTO = "listo", "Listo"
        ERROR = "error", "Error"

    uuid_publico = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text="Identificador público para compartir la evaluación sin exponer el ID interno.",
    )

    # Paso 1: Rubro
    rubro = models.CharField(max_length=20, choices=Rubro.choices)

    # Paso 2: Ciudad y público objetivo
    ciudad = models.CharField(max_length=100)
    publico = models.CharField("público objetivo", max_length=200)

    # Paso 3: Idea y presupuesto
    descripcion = models.TextField(validators=[MinLengthValidator(30)])
    presupuesto_disponible = models.CharField(max_length=50, blank=True)

    # Resultado IA. Estructura esperada:
    # {
    #   "puntajes": {
    #       "innovacion": 0-100,
    #       "escalabilidad": 0-100,
    #       "mercado": 0-100,
    #       "originalidad": 0-100,
    #       "viabilidad": 0-100,
    #   },
    #   "puntaje_global": number,
    #   "veredicto_emoji": str,
    #   "veredicto_titulo": str,
    #   "veredicto_texto": str,
    #   "foda": {
    #       "fortalezas": [],
    #       "oportunidades": [],
    #       "debilidades": [],
    #       "amenazas": [],
    #   },
    #   "presupuesto": {"mvp": str, "lanzamiento": str, "escala": str, "notas": str},
    #   "factibilidad": {
    #       "tecnica": {"nivel": str, "descripcion": str},
    #       "financiera": {"nivel": str, "descripcion": str},
    #       "legal": {"nivel": str, "descripcion": str},
    #       "mercado": {"nivel": str, "descripcion": str},
    #   },
    #   "competencia": [{"nombre": str, "descripcion": str, "tipo": str, "url": str}],
    #   "recomendaciones": [],
    # }
    resultado = models.JSONField(null=True, blank=True)

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
        db_index=True,
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    ip_origen = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["estado", "creado_en"], name="eval_estado_creado_idx"),
        ]
        verbose_name = "evaluación"
        verbose_name_plural = "evaluaciones"

    def __str__(self):
        fecha = self.creado_en.strftime("%d/%m/%Y") if self.creado_en else "sin fecha"
        return f"{self.get_rubro_display()} en {self.ciudad} · {self.publico} · {fecha}"
