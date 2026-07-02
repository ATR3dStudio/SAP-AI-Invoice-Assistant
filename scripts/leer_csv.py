import csv
import json

invoices = []
errors = []

vendors = ["Amazon", "IBM", "Microsoft", "SAP"]
currencies = ["EUR", "USD", "GBP"]

with open("data/facturas.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        supplier = row["supplier"]
        amount = int(row["amount"])
        currency = row["currency"]

        if supplier not in vendors:
            errors.append({
                "invoice": row,
                "reason": "Proveedor no registrado"
            })

        elif amount <= 0:
            errors.append({
                "invoice": row,
                "reason": "Importe menor o igual que cero"
            })

        elif currency not in currencies:
            errors.append({
                "invoice": row,
                "reason": "Moneda no valida"
            })

        else:
            invoice = {
                "supplier": supplier,
                "amount": amount,
                "currency": currency
            }

            invoices.append(invoice)

with open("output/facturas.json", "w") as file:
    json.dump(invoices, file, indent=4)

with open("output/errores.txt", "w") as file:
    for error in errors:
        invoice = error["invoice"]

        file.write("Proveedor: " + invoice["supplier"] + "\n")
        file.write("Importe: " + invoice["amount"] + "\n")
        file.write("Moneda: " + invoice["currency"] + "\n")
        file.write("ERROR: " + error["reason"] + "\n")
        file.write("-------------------------\n")

print("Proceso completado")