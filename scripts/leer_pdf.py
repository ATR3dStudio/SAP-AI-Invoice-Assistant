from pypdf import PdfReader
import json
import os
from datetime import datetime
from validar_factura import validar_factura
from ai_assistant import explicar_incidencia


def buscar_valor(lines, etiqueta):
    for i, line in enumerate(lines):
        if line.strip() == etiqueta:
            return lines[i + 1].strip()
    return ""


procesados = 0
errores = 0
log = []
informe_ia = []
ai_analysis = []

carpeta_pdf = "input/pdf"

for archivo in os.listdir(carpeta_pdf):

    if archivo.endswith(".pdf"):

        try:
            ruta_pdf = os.path.join(carpeta_pdf, archivo)

            print(f"\nProcesando {archivo}")

            reader = PdfReader(ruta_pdf)
            page = reader.pages[0]
            text = page.extract_text()
            lines = text.split("\n")

            supplier = lines[0].strip()
            invoice_number = buscar_valor(lines, "Invoice Number:")
            invoice_date = buscar_valor(lines, "Invoice Date:")
            due_date = buscar_valor(lines, "Due Date:")
            currency = buscar_valor(lines, "Currency")
            amount = buscar_valor(lines, "Total Amount")

            invoice_base = {
                "supplier": supplier,
                "invoice_number": invoice_number,
                "invoice_date": invoice_date,
                "due_date": due_date,
                "amount": amount,
                "currency": currency
            }

            resultado_validacion = validar_factura(invoice_base)

            invoice = {
                "supplier": supplier,
                "invoice_number": invoice_number,
                "invoice_date": invoice_date,
                "due_date": due_date,
                "amount": amount,
                "currency": currency,
                "validation": {
                    "status": resultado_validacion["estado"],
                    "errors": resultado_validacion["errores"]
                }
            }

            nombre_json = archivo.replace(".pdf", ".json")
            ruta_json = os.path.join("output", nombre_json)

            with open(ruta_json, "w", encoding="utf-8") as file:
                json.dump(invoice, file, indent=4, ensure_ascii=False)

            log.append({
                "archivo": archivo,
                "estado": resultado_validacion["estado"],
                "proveedor": supplier,
                "factura": invoice_number,
                "importe": amount,
                "errores": resultado_validacion["errores"],
                "fecha_proceso": str(datetime.now())
            })

            if resultado_validacion["estado"] == "OK":
                print(f"✅ {archivo} validado correctamente")
                procesados += 1

            else:
                print(f"❌ {archivo} rechazado")
                print("🤖 Generando explicación IA...")

                explicacion = explicar_incidencia(
                    invoice,
                    resultado_validacion["errores"]
                )

                try:
                    explicacion_json = json.loads(explicacion)

                except Exception:
                    explicacion_json = {
                        "summary": "No se pudo interpretar la respuesta de la IA.",
                        "severity": "UNKNOWN",
                        "sap_module": "-",
                        "business_impact": "-",
                        "recommended_action": "-",
                        "btp_service": "-"
                    }

                ai_item = {
                    "archivo": archivo,
                    "invoice_number": invoice_number,
                    "supplier": supplier,
                    "status": resultado_validacion["estado"],
                    "errors": resultado_validacion["errores"],
                    "ai": explicacion_json
                }

                ai_analysis.append(ai_item)

                informe_ia.append({
                    "archivo": archivo,
                    "invoice": invoice,
                    "ai": explicacion_json
                })

                errores += 1

        except Exception as e:
            log.append({
                "archivo": archivo,
                "estado": "ERROR_TECNICO",
                "motivo": str(e),
                "fecha_proceso": str(datetime.now())
            })

            print(f"❌ Error técnico en {archivo}")
            print(e)
            errores += 1


with open("output/procesamiento.log", "w", encoding="utf-8") as file:

    file.write("LOG DE PROCESAMIENTO DE FACTURAS\n")
    file.write("=================================\n\n")

    for registro in log:

        file.write("---------------------------------\n")
        file.write(f"Archivo: {registro['archivo']}\n")
        file.write(f"Estado: {registro['estado']}\n")

        if registro["estado"] == "OK":
            file.write(f"Proveedor: {registro['proveedor']}\n")
            file.write(f"Factura: {registro['factura']}\n")
            file.write(f"Importe: {registro['importe']}\n")

        elif registro["estado"] == "RECHAZADA":
            file.write(f"Proveedor: {registro['proveedor']}\n")
            file.write(f"Factura: {registro['factura']}\n")
            file.write(f"Importe: {registro['importe']}\n")
            file.write("Motivos de rechazo:\n")

            for error in registro["errores"]:
                file.write(f"- {error}\n")

        else:
            file.write(f"Motivo técnico: {registro['motivo']}\n")

        file.write(f"Fecha proceso: {registro['fecha_proceso']}\n")


    file.write("\n=================================\n")
    file.write("RESUMEN\n")
    file.write("=================================\n")
    file.write(f"Procesadas OK: {procesados}\n")
    file.write(f"Errores/Rechazadas: {errores}\n")


with open("output/ai_analysis.json", "w", encoding="utf-8") as file:
    json.dump(ai_analysis, file, indent=4, ensure_ascii=False)


with open("output/informe_ia.txt", "w", encoding="utf-8") as file:

    file.write("INFORME IA - FACTURAS RECHAZADAS\n")
    file.write("=================================\n\n")

    if len(informe_ia) == 0:
        file.write("No hay facturas rechazadas para analizar.\n")

    for item in informe_ia:

        ia = item["ai"]

        file.write(f"Archivo: {item['archivo']}\n")
        file.write("=" * 60 + "\n\n")

        file.write(f"Resumen: {ia['summary']}\n\n")
        file.write(f"Severidad: {ia['severity']}\n\n")
        file.write(f"Módulo SAP: {ia['sap_module']}\n\n")
        file.write(f"Impacto: {ia['business_impact']}\n\n")
        file.write(f"Acción recomendada: {ia['recommended_action']}\n\n")
        file.write(f"Servicio SAP BTP: {ia['btp_service']}\n\n")

        file.write("-" * 60 + "\n\n")


print("\n=================================")
print("RESUMEN")
print("=================================")
print(f"Procesadas OK: {procesados}")
print(f"Errores/Rechazadas: {errores}")
print("\nLog generado en output/procesamiento.log")
print("Informe IA generado en output/informe_ia.txt")
print("Análisis IA generado en output/ai_analysis.json")