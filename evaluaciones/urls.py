"""URL routes for business idea evaluations."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.evaluaciones_root, name='evaluaciones_root'),
]
