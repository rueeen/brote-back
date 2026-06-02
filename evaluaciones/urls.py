"""URL routes for evaluation endpoints."""

from django.urls import path

from .health import HealthCheckView
from .views import EvaluacionDetalleView, EvaluacionListView, EvaluarIdeaView

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health"),
    path("evaluar/", EvaluarIdeaView.as_view(), name="evaluar-idea"),
    path("evaluacion/<uuid:uuid>/", EvaluacionDetalleView.as_view(), name="evaluacion-detalle"),
    path("evaluaciones/", EvaluacionListView.as_view(), name="evaluacion-list"),
]
