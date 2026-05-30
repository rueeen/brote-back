"""URL routes for evaluation endpoints."""

from django.urls import path

from .views import EvaluacionDetalleView, EvaluacionListView, EvaluarIdeaView

urlpatterns = [
    path("evaluar/", EvaluarIdeaView.as_view(), name="evaluar-idea"),
    path("evaluacion/<uuid:uuid>/", EvaluacionDetalleView.as_view(), name="evaluacion-detalle"),
    path("evaluaciones/", EvaluacionListView.as_view(), name="evaluacion-list"),
]
