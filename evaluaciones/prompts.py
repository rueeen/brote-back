"""Prompt builders and validation helpers for AI business evaluations."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


CITY_CONTEXTS = {
    "santiago": (
        "Santiago: mercado metropolitano grande y competitivo, alta penetración "
        "digital, acceso a talento, inversión, corporativos y clientes B2B; costos "
        "de adquisición y arriendo más altos."
    ),
    "arica": (
        "Arica: ciudad fronteriza con oportunidades de comercio binacional, "
        "logística, turismo y conexión con Perú/Bolivia; mercado local más pequeño "
        "que exige foco en nichos y alianzas regionales."
    ),
    "valparaiso": (
        "Valparaíso: ecosistema creativo, portuario, turístico y universitario; "
        "buen potencial para economía creativa, servicios, cultura y soluciones "
        "vinculadas a comercio exterior."
    ),
    "concepcion": (
        "Concepción: polo universitario e industrial del Biobío, talento técnico, "
        "base de clase media y cercanía a sectores forestal, manufactura, salud y "
        "servicios avanzados."
    ),
    "temuco": (
        "Temuco: capital regional con oportunidades en agroindustria, turismo, "
        "educación, salud, comercio local y soluciones con pertinencia territorial "
        "para La Araucanía."
    ),
}

DEFAULT_CITY_CONTEXT = (
    "Otra ciudad chilena: mercado regional con escala inicial acotada, relevancia "
    "de redes locales, municipalidades, gremios, cámaras de comercio y alianzas "
    "para validar demanda antes de expandirse a otras regiones."
)

RUBRO_CONTEXTS = {
    "tecnologia": (
        "Tecnología: evaluar diferenciación técnica, velocidad de desarrollo, "
        "ciberseguridad, adopción digital, posibilidad SaaS/API y escalamiento "
        "nacional o regional."
    ),
    "gastronomia": (
        "Gastronomía: considerar costos de insumos, permisos sanitarios, delivery, "
        "ubicación, rotación, experiencia de marca y sensibilidad al precio del "
        "consumidor chileno."
    ),
    "retail": (
        "Retail: analizar inventario, márgenes, omnicanalidad, e-commerce, logística "
        "de última milla, competencia de marketplaces y diferenciación de propuesta."
    ),
    "salud": (
        "Salud: revisar confianza, evidencia, privacidad de datos, regulación, "
        "integración con prestadores, tiempos de venta B2B y barreras legales o "
        "clínicas."
    ),
    "educacion": (
        "Educación: ponderar resultados de aprendizaje, adopción por instituciones, "
        "venta B2B/B2C, retención, accesibilidad y pertinencia curricular chilena."
    ),
    "servicios": (
        "Servicios: evaluar calidad operacional, estandarización, recurrencia, "
        "capacidad de contratación, reputación, tiempos de atención y escalabilidad "
        "sin perder experiencia."
    ),
    "sustentabilidad": (
        "Sustentabilidad: considerar impacto medible, economía circular, regulación "
        "ambiental, alianzas público-privadas, disposición a pagar y potencial de "
        "financiamiento verde."
    ),
    "otro": (
        "Otro rubro: identificar claramente categoría, cliente, canal, sustitutos, "
        "barreras de entrada y supuestos críticos para validar en el mercado chileno."
    ),
}

REQUIRED_RESPONSE_SCHEMA = {
    "puntajes": {
        "innovacion": int,
        "escalabilidad": int,
        "mercado": int,
        "originalidad": int,
        "viabilidad": int,
    },
    "puntaje_global": int,
    "veredicto_emoji": str,
    "veredicto_titulo": str,
    "veredicto_texto": str,
    "foda": {
        "fortalezas": list,
        "oportunidades": list,
        "debilidades": list,
        "amenazas": list,
    },
    "presupuesto": {
        "mvp": str,
        "lanzamiento": str,
        "escala": str,
        "notas": str,
    },
    "factibilidad": {
        "tecnica": {"nivel": str, "descripcion": str},
        "financiera": {"nivel": str, "descripcion": str},
        "legal": {"nivel": str, "descripcion": str},
        "mercado": {"nivel": str, "descripcion": str},
    },
    "competencia": list,
    "recomendaciones": list,
}

FACTIBILIDAD_NIVELES = {"Alta", "Media", "Baja"}
COMPETENCIA_TIPOS = {"directa", "indirecta", "ninguna"}


def _normalize_key(value: Any) -> str:
    """Return a lowercase key suitable for context lookups."""
    return str(value or "").strip().lower()


def _get_city_context(city: Any) -> str:
    """Return Chile-specific local market context for the provided city."""
    return CITY_CONTEXTS.get(_normalize_key(city), DEFAULT_CITY_CONTEXT)


def _get_rubro_context(rubro: Any) -> str:
    """Return business vertical context for the provided category."""
    return RUBRO_CONTEXTS.get(_normalize_key(rubro), RUBRO_CONTEXTS["otro"])


def build_prompt(data: dict) -> str:
    """
    Build Claude's prompt for evaluating a Chilean business idea.

    Expected input keys are: rubro, publico, descripcion, ciudad and optionally
    presupuesto_disponible.
    """
    rubro = data.get("rubro", "otro")
    publico = data.get("publico", "No especificado")
    descripcion = data.get("descripcion", "")
    ciudad = data.get("ciudad", "Otra")
    presupuesto = data.get("presupuesto_disponible") or "No especificado"
    contexto_ciudad = _get_city_context(ciudad)
    contexto_rubro = _get_rubro_context(rubro)

    return f"""Eres Claude, actuando como analista experto en startups, innovación, finanzas tempranas y mercado chileno.
Evalúa una idea de negocio para una plataforma chilena llamada BROTE, orientada a emprendedores que necesitan feedback claro, accionable y realista.

CONTEXTO CHILENO OBLIGATORIO
- Considera el ecosistema emprendedor chileno: CORFO, Start-Up Chile, incubadoras/aceleradoras, universidades, fondos públicos, redes regionales y validación con clientes del mercado local.
- Evalúa la propuesta según condiciones reales de Chile: tamaño de mercado, poder adquisitivo, confianza del consumidor, informalidad, canales digitales, logística, regulación sectorial y competencia local.
- Si corresponde, menciona oportunidades o riesgos para postular a instrumentos de CORFO, Start-Up Chile u otras redes de apoyo, pero sin asumir que la idea será financiada.

CONTEXTO POR CIUDAD
{contexto_ciudad}

CONTEXTO POR RUBRO
{contexto_rubro}

DATOS DE LA IDEA
- Rubro: {rubro}
- Público objetivo: {publico}
- Ciudad/mercado inicial: {ciudad}
- Presupuesto disponible aproximado: {presupuesto}
- Descripción: {descripcion}

INSTRUCCIONES DE EVALUACIÓN
- Sé exigente, específico y útil para un emprendedor chileno en etapa temprana.
- Usa puntajes enteros de 0 a 100; el puntaje_global debe ser consistente con los cinco puntajes parciales.
- Entrega FODA con elementos concretos, no genéricos.
- Estima presupuesto en rangos USD realistas para MVP, lanzamiento y escala inicial; aclara supuestos en notas.
- En competencia, incluye competidores o sustitutos conocidos cuando puedas inferirlos; si no hay datos suficientes, usa tipo "ninguna" con explicación y url vacía.
- Las recomendaciones deben ser accionables, priorizadas y adecuadas a la ciudad, rubro y presupuesto.

FORMATO DE RESPUESTA OBLIGATORIO
Responde SOLO con JSON válido, sin backticks, sin markdown, sin comentarios y sin texto extra antes o después.
Respeta exactamente estas claves de primer nivel y estructura:
{{
  "puntajes": {{
    "innovacion": 0,
    "escalabilidad": 0,
    "mercado": 0,
    "originalidad": 0,
    "viabilidad": 0
  }},
  "puntaje_global": 0,
  "veredicto_emoji": "emoji",
  "veredicto_titulo": "título corto",
  "veredicto_texto": "2-3 oraciones",
  "foda": {{
    "fortalezas": [],
    "oportunidades": [],
    "debilidades": [],
    "amenazas": []
  }},
  "presupuesto": {{
    "mvp": "rango USD",
    "lanzamiento": "rango USD",
    "escala": "rango USD",
    "notas": "texto"
  }},
  "factibilidad": {{
    "tecnica": {{ "nivel": "Alta|Media|Baja", "descripcion": "texto" }},
    "financiera": {{ "nivel": "Alta|Media|Baja", "descripcion": "texto" }},
    "legal": {{ "nivel": "Alta|Media|Baja", "descripcion": "texto" }},
    "mercado": {{ "nivel": "Alta|Media|Baja", "descripcion": "texto" }}
  }},
  "competencia": [
    {{ "nombre": "", "descripcion": "", "tipo": "directa|indirecta|ninguna", "url": "" }}
  ],
  "recomendaciones": ["rec1", "rec2", "rec3"]
}}"""


def construir_prompt(data: dict) -> str:
    """Backward-compatible alias for older imports."""
    return build_prompt(data)


def _validate_schema(data: Any, schema: Any) -> bool:
    """Recursively verify required keys and value container types."""
    if isinstance(schema, dict):
        if not isinstance(data, Mapping):
            return False
        return all(key in data and _validate_schema(data[key], value) for key, value in schema.items())

    if isinstance(schema, type):
        return isinstance(data, schema)

    return True


def _is_score(value: Any) -> bool:
    """Return True when value is an integer score in the 0-100 range."""
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 100


def _is_string_list(value: Any) -> bool:
    """Return True when value is a list of strings."""
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _validate_competencia(items: Any) -> bool:
    """Validate the competition entries expected from Claude."""
    if not isinstance(items, list):
        return False

    required_keys = {"nombre", "descripcion", "tipo", "url"}
    for item in items:
        if not isinstance(item, Mapping) or not required_keys.issubset(item):
            return False
        if item["tipo"] not in COMPETENCIA_TIPOS:
            return False
        if not all(isinstance(item[key], str) for key in required_keys):
            return False

    return True


def validate_ai_response(data: dict) -> bool:
    """
    Validate Claude's JSON structure before saving it as an evaluation result.

    This verifies all required keys, basic value types, score ranges, allowed
    factibility levels and competition item shape.
    """
    if not _validate_schema(data, REQUIRED_RESPONSE_SCHEMA):
        return False

    if not all(_is_score(score) for score in data["puntajes"].values()):
        return False
    if not _is_score(data["puntaje_global"]):
        return False

    if not all(_is_string_list(data["foda"][key]) for key in REQUIRED_RESPONSE_SCHEMA["foda"]):
        return False
    if not _is_string_list(data["recomendaciones"]):
        return False

    for value in data["factibilidad"].values():
        if value["nivel"] not in FACTIBILIDAD_NIVELES:
            return False

    return _validate_competencia(data["competencia"])
