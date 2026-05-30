import json

from anthropic import Anthropic
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Evaluacion
from .prompts import construir_prompt
from .serializers import EvaluacionInputSerializer

client = Anthropic(api_key=config("ANTHROPIC_API_KEY"))


class EvaluarIdeaView(APIView):
    def post(self, request):
        serializer = EvaluacionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        evaluacion = Evaluacion.objects.create(
            **data,
            estado=Evaluacion.Estado.PROCESANDO,
            ip_origen=request.META.get("REMOTE_ADDR"),
        )

        try:
            prompt = construir_prompt(data)
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            texto = message.content[0].text.strip()
            resultado = json.loads(texto)

            evaluacion.resultado = resultado
            evaluacion.estado = Evaluacion.Estado.LISTO
            evaluacion.save(update_fields=["resultado", "estado", "actualizado_en"])

            return Response(
                {"uuid_publico": evaluacion.uuid_publico, "resultado": resultado},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            evaluacion.estado = Evaluacion.Estado.ERROR
            evaluacion.save(update_fields=["estado", "actualizado_en"])
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EvaluacionDetalleView(APIView):
    """Recuperar una evaluación guardada por UUID público."""

    def get(self, request, uuid_publico):
        try:
            ev = Evaluacion.objects.get(uuid_publico=uuid_publico)
            return Response(
                {
                    "uuid_publico": ev.uuid_publico,
                    "estado": ev.estado,
                    "resultado": ev.resultado,
                }
            )
        except Evaluacion.DoesNotExist:
            return Response({"error": "No encontrada"}, status=status.HTTP_404_NOT_FOUND)
