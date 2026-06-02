"""Health-check endpoint for the BROTE backend."""

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """Return the public health status for the backend service."""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                "status": "ok",
                "servicio": "brote-backend",
                "version": "0.1.0",
            }
        )
