"""URL routes for user-related features."""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.usuarios_root, name='usuarios_root'),
]
