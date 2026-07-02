from openai import OpenAI

client = OpenAI()


def explicar_incidencia(invoice, errores):
    prompt = f"""
Actúa como consultor SAP FI/MM y SAP BTP.

Analiza esta factura rechazada y explica la incidencia de forma clara,
funcional y orientada a negocio.

Factura:
{invoice}

Errores detectados:
{errores}

Devuelve EXCLUSIVAMENTE un JSON válido.

Debe tener exactamente esta estructura:

{{
    "summary": "...",
    "severity": "LOW | MEDIUM | HIGH",
    "sap_module": "...",
    "business_impact": "...",
    "recommended_action": "...",
    "btp_service": "..."
}}

No escribas absolutamente nada fuera del JSON.
No añadas markdown.
No añadas comillas triples.
No añadas explicaciones.
Usa un tono profesional, claro y útil para un usuario de negocio.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text