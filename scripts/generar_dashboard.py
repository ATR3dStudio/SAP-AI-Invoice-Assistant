import os
import json

carpeta_output = "output"
facturas = []
analisis_ia = {}

for archivo in os.listdir(carpeta_output):

    if archivo.endswith(".json"):

        ruta = os.path.join(carpeta_output, archivo)

        with open(ruta, "r", encoding="utf-8") as f:
            contenido = json.load(f)

        if archivo == "ai_analysis.json":
            for item in contenido:
                analisis_ia[item["invoice_number"]] = item

        elif isinstance(contenido, dict) and "validation" in contenido:
            facturas.append(contenido)

html = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>SAP AI Invoice Assistant</title>

<style>
body {
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    margin: 40px;
    color: #1f2933;
}

h1 {
    color: #0a6ed1;
    margin-bottom: 5px;
}

.subtitle {
    color: #52616b;
    margin-bottom: 30px;
}

.summary {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
}

.summary-card {
    background: white;
    border-radius: 12px;
    padding: 18px;
    width: 220px;
    box-shadow: 0 3px 10px rgba(0,0,0,.12);
}

.summary-card h2 {
    margin: 0;
    font-size: 30px;
}

.card {
    background: white;
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 22px;
    box-shadow: 0 3px 10px rgba(0,0,0,.12);
    border-left: 6px solid #0a6ed1;
}

.card.ok {
    border-left-color: #2e7d32;
}

.card.error {
    border-left-color: #c62828;
}

.status-ok {
    color: #2e7d32;
    font-weight: bold;
}

.status-error {
    color: #c62828;
    font-weight: bold;
}

.severity-high {
    color: #c62828;
    font-weight: bold;
}

.severity-medium {
    color: #ef6c00;
    font-weight: bold;
}

.severity-low {
    color: #2e7d32;
    font-weight: bold;
}

table {
    width: 100%;
    margin-bottom: 15px;
}

td {
    padding: 6px;
    vertical-align: top;
}

.ai-box {
    background: #eef6ff;
    border-radius: 10px;
    padding: 15px;
    margin-top: 15px;
}

.ai-box h3 {
    margin-top: 0;
    color: #0a6ed1;
}

.label {
    font-weight: bold;
    width: 180px;
}
</style>
</head>

<body>

<h1>SAP AI Invoice Assistant</h1>
<p>
Enterprise Invoice Validation Dashboard
</p>

<p>
Proyecto demostrativo • SAP FI • SAP BTP • IA • Python
</p>
<div class="subtitle">Dashboard inteligente de validación documental inspirado en procesos SAP FI/MM + BTP</div>
"""

total = len(facturas)
ok = sum(1 for f in facturas if f["validation"]["status"] == "OK")
rechazadas = total - ok
analizadas_ia = len(analisis_ia)

html += f"""

<div class="summary">

    <div class="summary-card">
        <div>📄 Facturas analizadas</div>
        <h2>{total}</h2>
    </div>

    <div class="summary-card">
        <div>✅ Correctas</div>
        <h2>{ok}</h2>
    </div>

    <div class="summary-card">
        <div>❌ Rechazadas</div>
        <h2>{rechazadas}</h2>
    </div>

    <div class="summary-card">
        <div>🤖 Analizadas por IA</div>
        <h2>{analizadas_ia}</h2>
    </div>

</div>

"""

for factura in facturas:

    estado = factura["validation"]["status"]
    clase_card = "ok" if estado == "OK" else "error"
    clase_estado = "status-ok" if estado == "OK" else "status-error"

    invoice_number = factura.get("invoice_number", "")
    ai_item = analisis_ia.get(invoice_number)

    html += f"""
<div class="card {clase_card}">
<h2>{factura.get("supplier", "-")}</h2>

<table>
<tr><td class="label">Factura</td><td>{invoice_number}</td></tr>
<tr><td class="label">Fecha factura</td><td>{factura.get("invoice_date", "-")}</td></tr>
<tr><td class="label">Vencimiento</td><td>{factura.get("due_date", "-")}</td></tr>
<tr><td class="label">Importe</td><td>{factura.get("amount", "-")}</td></tr>
<tr><td class="label">Moneda</td><td>{factura.get("currency", "-")}</td></tr>
<tr><td class="label">Estado</td><td class="{clase_estado}">{estado}</td></tr>
</table>
"""

    if estado != "OK":
        errores = factura["validation"]["errors"]

        html += "<b>Motivos de rechazo:</b><ul>"
        for error in errores:
            html += f"<li>{error}</li>"
        html += "</ul>"

        if ai_item:
            ia = ai_item["ai"]
            severity = ia.get("severity", "UNKNOWN")
            severity_class = f"severity-{severity.lower()}" if severity.lower() in ["high", "medium", "low"] else ""

            html += f"""
<div class="ai-box">
<h3>🤖 Análisis IA</h3>
<table>
<tr><td class="label">Resumen</td><td>{ia.get("summary", "-")}</td></tr>
<tr><td class="label">Severidad</td><td class="{severity_class}">{severity}</td></tr>
<tr><td class="label">Módulo SAP</td><td>{ia.get("sap_module", "-")}</td></tr>
<tr><td class="label">Impacto negocio</td><td>{ia.get("business_impact", "-")}</td></tr>
<tr><td class="label">Acción recomendada</td><td>{ia.get("recommended_action", "-")}</td></tr>
<tr><td class="label">Servicio BTP</td><td>{ia.get("btp_service", "-")}</td></tr>
</table>
</div>
"""

    html += "</div>"

html += """
</body>
</html>
"""

with open("dashboard.html", "w", encoding="utf-8") as file:
    file.write(html)

print("Dashboard inteligente generado correctamente.")