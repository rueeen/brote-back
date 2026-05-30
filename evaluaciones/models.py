from django.db import models

# Create your models here.
from django.db import models

class Evaluacion(models.Model):
    RUBROS = [
        ('tecnologia', 'Tecnología'),
        ('gastronomia', 'Gastronomía'),
        ('retail', 'Retail'),
        ('salud', 'Salud'),
        ('educacion', 'Educación'),
        ('servicios', 'Servicios'),
        ('sustentabilidad', 'Sustentabilidad'),
        ('otro', 'Otro'),
    ]

    # Datos del formulario
    rubro         = models.CharField(max_length=50, choices=RUBROS)
    publico       = models.CharField(max_length=200)   # público objetivo
    descripcion   = models.TextField()
    ciudad        = models.CharField(max_length=100)
    presupuesto_disponible = models.CharField(max_length=50, blank=True)  # opcional

    # Resultado IA
    resultado     = models.JSONField(null=True, blank=True)
    estado        = models.CharField(
        max_length=20,
        choices=[('pendiente','Pendiente'),('procesando','Procesando'),('listo','Listo'),('error','Error')],
        default='pendiente'
    )

    # Metadata
    creado_en     = models.DateTimeField(auto_now_add=True)
    ip_origen     = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.rubro} — {self.ciudad} ({self.creado_en:%d/%m/%Y})"
