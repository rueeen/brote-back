"""Views for business idea evaluations."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def evaluaciones_root(request):
    """Return a basic health response for the evaluations API."""
    return Response({'detail': 'Evaluaciones API lista.'})

from django.shortcuts import render

# Create your views here.
import json
from anthropic import Anthropic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from .models import Evaluacion
from .serializers import EvaluacionInputSerializer
from .prompts import build_prompt, validate_ai_response


def get_anthropic_client():
    """Create an Anthropic client when an evaluation is requested."""
    return Anthropic(api_key=config("ANTHROPIC_API_KEY"))


class EvaluarIdeaView(APIView):
    def post(self, request):
        serializer = EvaluacionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data
        evaluacion = Evaluacion.objects.create(
            **data,
            estado='procesando',
            ip_origen=request.META.get('REMOTE_ADDR')
        )

        try:
            prompt = build_prompt(data)
            message = get_anthropic_client().messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            texto = message.content[0].text.strip()
            resultado = json.loads(texto)
            if not validate_ai_response(resultado):
                raise ValueError("La respuesta de Claude no cumple el esquema requerido.")

            evaluacion.resultado = resultado
            evaluacion.estado = 'listo'
            evaluacion.save()

            return Response({"id": evaluacion.id, "resultado": resultado}, status=200)

        except Exception as e:
            evaluacion.estado = 'error'
            evaluacion.save()
            return Response({"error": str(e)}, status=500)


class EvaluacionDetalleView(APIView):
    """Recuperar una evaluación guardada por ID"""
    def get(self, request, pk):
        try:
            ev = Evaluacion.objects.get(pk=pk)
            return Response({"id": ev.id, "estado": ev.estado, "resultado": ev.resultado})
        except Evaluacion.DoesNotExist:
            return Response({"error": "No encontrada"}, status=404)