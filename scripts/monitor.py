import os
import json

carpeta_output = "output"

correctas = 0
rechazadas = 0

facturas = []

for archivo in os.listdir(carpeta_output):

    if archivo.startswith("factura_") and archivo.endswith(".json"):

        ruta = os.path.join(carpeta_output, archivo)

        with open(ruta, "r", encoding="utf-8") as file:

            factura = json.load(file)

            facturas.append(factura)

            if factura["supplier"] == "AMAZON BUSINESS EU S.A.R.L.":

                correctas += 1

            else:

                rechazadas += 1

print()

print("=" * 50)

print(" SAP AI INVOICE ASSISTANT")

print("=" * 50)

print()

print(f"Facturas encontradas : {len(facturas)}")

print(f"Correctas            : {correctas}")

print(f"Rechazadas           : {rechazadas}")

print()

print("-" * 50)

print("FACTURAS")

print("-" * 50)

for factura in facturas:

    print()

    print("Proveedor :", factura["supplier"])

    print("Factura   :", factura["invoice_number"])

    print("Importe   :", factura["amount"])

    print("Moneda    :", factura["currency"])

print()

print("=" * 50)