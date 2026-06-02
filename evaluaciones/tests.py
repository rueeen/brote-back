from unittest import TestCase

from django.test import Client, SimpleTestCase
from django.urls import Resolver404, resolve

from .prompts import build_prompt, construir_prompt, validate_ai_response


VALID_AI_RESPONSE = {
    "puntajes": {
        "innovacion": 80,
        "escalabilidad": 75,
        "mercado": 70,
        "originalidad": 82,
        "viabilidad": 68,
    },
    "puntaje_global": 75,
    "veredicto_emoji": "🌱",
    "veredicto_titulo": "Buen potencial",
    "veredicto_texto": "La idea tiene oportunidades claras en Chile. Debe validar demanda y costos antes de escalar.",
    "foda": {
        "fortalezas": ["Propuesta clara"],
        "oportunidades": ["Apoyo CORFO"],
        "debilidades": ["Presupuesto limitado"],
        "amenazas": ["Competidores locales"],
    },
    "presupuesto": {
        "mvp": "USD 2.000-5.000",
        "lanzamiento": "USD 5.000-12.000",
        "escala": "USD 15.000-40.000",
        "notas": "Validar con pilotos locales.",
    },
    "factibilidad": {
        "tecnica": {"nivel": "Alta", "descripcion": "Se puede construir con tecnología disponible."},
        "financiera": {"nivel": "Media", "descripcion": "Requiere controlar CAC."},
        "legal": {"nivel": "Media", "descripcion": "Revisar permisos aplicables."},
        "mercado": {"nivel": "Alta", "descripcion": "Existe demanda inicial."},
    },
    "competencia": [
        {
            "nombre": "Competidor local",
            "descripcion": "Alternativa existente en el mercado.",
            "tipo": "indirecta",
            "url": "",
        }
    ],
    "recomendaciones": ["Validar problema", "Probar MVP", "Medir retención"],
}


class HealthEndpointTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_health_endpoint_returns_public_service_status(self):
        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "servicio": "brote-backend",
                "version": "0.1.0",
            },
        )

    def test_usuarios_root_is_not_registered(self):
        with self.assertRaises(Resolver404):
            resolve("/api/usuarios/")


class PromptBuilderTests(TestCase):
    def test_build_prompt_includes_chilean_city_rubro_and_json_instructions(self):
        prompt = build_prompt(
            {
                "rubro": "tecnologia",
                "publico": "pymes chilenas",
                "descripcion": "Software para automatizar reservas y pagos de pequeñas empresas.",
                "ciudad": "Temuco",
                "presupuesto_disponible": "USD 3.000",
            }
        )

        self.assertIn("Temuco", prompt)
        self.assertIn("La Araucanía", prompt)
        self.assertIn("Tecnología", prompt)
        self.assertIn("CORFO", prompt)
        self.assertIn("Start-Up Chile", prompt)
        self.assertIn("mercado local", prompt)
        self.assertIn("Responde SOLO con JSON válido", prompt)
        self.assertIn("sin backticks", prompt)
        self.assertIn('"puntajes"', prompt)
        self.assertIn('"competencia"', prompt)

    def test_construir_prompt_alias_matches_build_prompt(self):
        data = {
            "rubro": "retail",
            "publico": "consumidores regionales",
            "descripcion": "Marketplace para productos locales con despacho colaborativo.",
            "ciudad": "Valparaíso",
        }

        self.assertEqual(construir_prompt(data), build_prompt(data))


class ValidateAiResponseTests(TestCase):
    def test_validate_ai_response_accepts_required_schema(self):
        self.assertTrue(validate_ai_response(VALID_AI_RESPONSE))

    def test_validate_ai_response_rejects_missing_required_key(self):
        invalid_response = VALID_AI_RESPONSE.copy()
        invalid_response.pop("presupuesto")

        self.assertFalse(validate_ai_response(invalid_response))

    def test_validate_ai_response_rejects_out_of_range_scores(self):
        invalid_response = {
            **VALID_AI_RESPONSE,
            "puntajes": {**VALID_AI_RESPONSE["puntajes"], "mercado": 101},
        }

        self.assertFalse(validate_ai_response(invalid_response))

    def test_validate_ai_response_rejects_invalid_factibilidad_level(self):
        invalid_response = {
            **VALID_AI_RESPONSE,
            "factibilidad": {
                **VALID_AI_RESPONSE["factibilidad"],
                "legal": {"nivel": "Regular", "descripcion": "No permitido."},
            },
        }

        self.assertFalse(validate_ai_response(invalid_response))
