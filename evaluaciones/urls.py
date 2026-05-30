from django.urls import path
from .views import EvaluarIdeaView, EvaluacionDetalleView

urlpatterns = [
    path('evaluar/', EvaluarIdeaView.as_view()),
    path('evaluacion/<int:pk>/', EvaluacionDetalleView.as_view()),
]
