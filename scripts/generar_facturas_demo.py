import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

input_file = "test_data/facturas_demo.json"
output_folder = "input/pdf"

os.makedirs(output_folder, exist_ok=True)

with open(input_file, "r", encoding="utf-8") as file:
    facturas = json.load(file)

for factura in facturas:
    supplier = factura["supplier"] if factura["supplier"] != "" else "UNKNOWN SUPPLIER"
    invoice_number = factura["invoice_number"] if factura["invoice_number"] != "" else "NO_INVOICE_NUMBER"

    file_name = f"{supplier}_{invoice_number}.pdf"
    file_name = file_name.replace(" ", "_").replace("/", "-")
    file_path = os.path.join(output_folder, file_name)

    pdf = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 80

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, supplier)
    y -= 40

    pdf.setFont("Helvetica", 11)

    pdf.drawString(50, y, "Invoice Number:")
    y -= 20
    pdf.drawString(50, y, factura["invoice_number"])
    y -= 30

    pdf.drawString(50, y, "Invoice Date:")
    y -= 20
    pdf.drawString(50, y, factura["invoice_date"])
    y -= 30

    pdf.drawString(50, y, "Due Date:")
    y -= 20
    pdf.drawString(50, y, factura["due_date"])
    y -= 30

    pdf.drawString(50, y, "Currency")
    y -= 20
    pdf.drawString(50, y, factura["currency"])
    y -= 30

    pdf.drawString(50, y, "Total Amount")
    y -= 20
    pdf.drawString(50, y, factura["amount"])

    pdf.save()

    print(f"PDF generado: {file_path}")

print("\nFacturas demo generadas correctamente.")