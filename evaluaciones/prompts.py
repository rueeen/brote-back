def construir_prompt(data: dict) -> str:
    """
    Construye el prompt enriquecido a partir del formulario multi-paso.
    data: { rubro, publico, descripcion, ciudad, presupuesto_disponible }
    """
    contexto_ciudad = {
        "santiago":  "mercado urbano competitivo, alta penetración digital, consumidor exigente",
        "arica":     "ciudad fronteriza con potencial de comercio binacional, mercado más pequeño pero fiel",
        "valparaiso":"ciudad creativa, turística, con fuerte cultura emprendedora",
        "concepcion":"polo universitario, alta adopción tecnológica, clase media consolidada",
    }.get(data["ciudad"].lower(), "mercado regional chileno")

    return f"""Eres un experto en evaluación de startups, emprendimiento latinoamericano e innovación.
Analiza la siguiente propuesta de negocio con profundidad y rigor.

═══════════════════════════════
DATOS DE LA IDEA
═══════════════════════════════
- Rubro:               {data['rubro']}
- Público objetivo:    {data['publico']}
- Ciudad/mercado:      {data['ciudad']} ({contexto_ciudad})
- Presupuesto aprox.:  {data.get('presupuesto_disponible') or 'No especificado'}

DESCRIPCIÓN DE LA IDEA:
{data['descripcion']}
═══════════════════════════════

Considera el contexto socioeconómico de Chile y Latinoamérica.
Responde SOLO con JSON válido (sin backticks, sin texto extra):

{{
  "puntajes": {{
    "innovacion":     <0-100>,
    "escalabilidad":  <0-100>,
    "mercado":        <0-100>,
    "originalidad":   <0-100>,
    "viabilidad":     <0-100>
  }},
  "puntaje_global": <0-100>,
  "veredicto_emoji":  "<emoji>",
  "veredicto_titulo": "<título corto impactante>",
  "veredicto_texto":  "<2-3 oraciones evaluando la idea en contexto>",

  "foda": {{
    "fortalezas":    ["<f1>", "<f2>", "<f3>"],
    "oportunidades": ["<o1>", "<o2>", "<o3>"],
    "debilidades":   ["<d1>", "<d2>", "<d3>"],
    "amenazas":      ["<a1>", "<a2>", "<a3>"]
  }},

  "presupuesto": {{
    "mvp":         "<rango en USD>",
    "lanzamiento": "<rango en USD>",
    "escala":      "<rango en USD>",
    "notas":       "<consideraciones específicas para {data['ciudad']}>"
  }},

  "factibilidad": {{
    "tecnica":    {{ "nivel": "<Alta|Media|Baja>", "descripcion": "<1-2 oraciones>" }},
    "financiera": {{ "nivel": "<Alta|Media|Baja>", "descripcion": "<1-2 oraciones>" }},
    "legal":      {{ "nivel": "<Alta|Media|Baja>", "descripcion": "<1-2 oraciones>" }},
    "mercado":    {{ "nivel": "<Alta|Media|Baja>", "descripcion": "<1-2 oraciones>" }}
  }},

  "competencia": [
    {{ "nombre": "<nombre>", "descripcion": "<1 frase>", "tipo": "directa|indirecta|ninguna", "url": "<url o null>" }}
  ],

  "recomendaciones": ["<rec1>", "<rec2>", "<rec3>"]
}}"""