"""API views for business idea evaluations."""

from __future__ import annotations

import hashlib
import json
from json import JSONDecodeError

from anthropic import Anthropic
from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Evaluacion
from .prompts import build_prompt, validate_ai_response
from .serializers import (
    EvaluacionInputSerializer,
    EvaluacionListSerializer,
    EvaluacionOutputSerializer,
)

RATE_LIMIT_MAX_REQUESTS = 5
RATE_LIMIT_WINDOW_SECONDS = 60 * 60
RATE_LIMIT_CACHE_PREFIX = "evaluar_idea_rate_limit"


def error_response(message: str, code: str, http_status: int) -> Response:
    """Return API errors with the standard BROTE error shape."""
    return Response(
        {"error": message, "codigo": code},
        status=http_status,
    )


def get_client_ip(request) -> str:
    """Resolve the client IP, considering common reverse-proxy headers."""
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR", "") or "0.0.0.0"


def get_rate_limit_key(ip_address: str) -> str:
    """Build a cache-safe key for the hourly IP rate limit."""
    ip_hash = hashlib.sha256(ip_address.encode("utf-8")).hexdigest()
    return f"{RATE_LIMIT_CACHE_PREFIX}:{ip_hash}"


def is_rate_limited(ip_address: str) -> bool:
    """Track requests per IP in LocMemCache and report if the limit is exceeded."""
    cache_key = get_rate_limit_key(ip_address)
    added = cache.add(cache_key, 1, timeout=RATE_LIMIT_WINDOW_SECONDS)
    if added:
        return False

    try:
        request_count = cache.incr(cache_key)
    except ValueError:
        cache.set(cache_key, 1, timeout=RATE_LIMIT_WINDOW_SECONDS)
        return False

    return request_count > RATE_LIMIT_MAX_REQUESTS


def get_anthropic_client() -> Anthropic:
    """Create an Anthropic client for an evaluation request."""
    return Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def extract_claude_text(message) -> str:
    """Extract the first text block returned by the Anthropic Messages API."""
    for block in getattr(message, "content", []):
        text = getattr(block, "text", None)
        if text:
            return text.strip()

    raise ValueError("Claude no devolvió contenido de texto.")


class EvaluarIdeaView(APIView):
    """Create and evaluate a business idea with Claude."""

    permission_classes = [AllowAny]

    def post(self, request):
        ip_address = get_client_ip(request)
        if is_rate_limited(ip_address):
            return error_response(
                "Has superado el máximo de 5 evaluaciones por IP por hora. Intenta nuevamente más tarde.",
                "RATE_LIMIT_EXCEDIDO",
                status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer = EvaluacionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                "Los datos enviados no son válidos.",
                "DATOS_INVALIDOS",
                status.HTTP_400_BAD_REQUEST,
            )

        data = serializer.validated_data
        evaluacion = Evaluacion.objects.create(
            **data,
            estado="procesando",
            ip_origen=ip_address,
        )

        try:
            prompt = build_prompt(data)
            message = get_anthropic_client().messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )
            resultado = json.loads(extract_claude_text(message))

            if not validate_ai_response(resultado):
                raise ValueError("La respuesta de Claude no cumple el esquema requerido.")

            evaluacion.resultado = resultado
            evaluacion.estado = "listo"
            evaluacion.save(update_fields=["resultado", "estado"])

            return Response(
                {"uuid": evaluacion.uuid, "resultado": resultado},
                status=status.HTTP_201_CREATED,
            )
        except JSONDecodeError:
            evaluacion.estado = "error"
            evaluacion.save(update_fields=["estado"])
            return error_response(
                "Claude devolvió una respuesta que no es JSON válido.",
                "RESPUESTA_IA_JSON_INVALIDO",
                status.HTTP_502_BAD_GATEWAY,
            )
        except ValueError as exc:
            evaluacion.estado = "error"
            evaluacion.save(update_fields=["estado"])
            return error_response(
                str(exc),
                "RESPUESTA_IA_INVALIDA",
                status.HTTP_502_BAD_GATEWAY,
            )
        except Exception:
            evaluacion.estado = "error"
            evaluacion.save(update_fields=["estado"])
            return error_response(
                "No pudimos completar la evaluación con IA. Intenta nuevamente más tarde.",
                "ERROR_EVALUACION_IA",
                status.HTTP_502_BAD_GATEWAY,
            )


class EvaluacionDetalleView(APIView):
    """Return a complete saved evaluation by UUID."""

    permission_classes = [AllowAny]

    def get(self, request, uuid):
        try:
            evaluacion = Evaluacion.objects.get(uuid=uuid)
        except Evaluacion.DoesNotExist:
            return error_response(
                "No encontramos una evaluación con ese UUID.",
                "EVALUACION_NO_ENCONTRADA",
                status.HTTP_404_NOT_FOUND,
            )

        return Response(EvaluacionOutputSerializer(evaluacion).data)


class EvaluacionListView(APIView):
    """List the latest evaluations without returning the full AI result."""

    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Evaluacion.objects.all().order_by("-creado_en")
        rubro = request.query_params.get("rubro")
        if rubro:
            queryset = queryset.filter(rubro=rubro)

        evaluaciones = queryset[:20]
        return Response(EvaluacionListSerializer(evaluaciones, many=True).data)
