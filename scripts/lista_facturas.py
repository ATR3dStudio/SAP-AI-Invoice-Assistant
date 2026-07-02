invoices = [
    {
        "supplier": "Amazon",
        "amount": 500
    },
    {
        "supplier": "IBM",
        "amount": 1000
    },
    {
        "supplier": "Microsoft",
        "amount": 250
    },
    {
    "supplier": "SAP",
    "amount": 750
}
]

total = 0

for invoice in invoices:

    total = total + invoice["amount"]

print("Total facturas:")
print(total)
print("Numero facturas:")
print(len(invoices))

average = total / len(invoices)

print("Importe medio:")
print(average)

max_amount = 0
max_supplier = ""

for invoice in invoices:

    if invoice["amount"] > max_amount:

        max_amount = invoice["amount"]
        max_supplier = invoice["supplier"]

print("Proveedor con factura mas alta:")
print(max_supplier)

print("Importe:")
print(max_amount)