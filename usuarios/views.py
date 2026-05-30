"""Views for user-related features."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def usuarios_root(request):
    """Return a basic health response for the users API."""
    return Response({'detail': 'Usuarios API lista.'})
