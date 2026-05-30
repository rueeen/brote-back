"""Views for business idea evaluations."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def evaluaciones_root(request):
    """Return a basic health response for the evaluations API."""
    return Response({'detail': 'Evaluaciones API lista.'})
