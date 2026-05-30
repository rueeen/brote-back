from django.urls import path

from .views import EvaluacionDetalleView, EvaluarIdeaView

urlpatterns = [
    path("evaluar/", EvaluarIdeaView.as_view()),
    path("evaluacion/<uuid:uuid_publico>/", EvaluacionDetalleView.as_view()),
]
