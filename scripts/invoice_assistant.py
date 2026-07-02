import json

vendors = ["Amazon", "Microsoft", "IBM"]
currencies = ["EUR", "USD", "GBP"]

supplier = input("Proveedor: ")

if supplier == "":
    print("ERROR: El proveedor es obligatorio")

elif supplier not in vendors:
    print("ERROR: Proveedor no encontrado")

else:

    invoice_number = input("Numero de factura: ")

    if invoice_number == "":
        print("ERROR: El numero de factura es obligatorio")

    else:

        try:

            amount = int(input("Importe: "))

            if amount <= 0:
                print("ERROR: El importe debe ser mayor que cero")

            else:

                currency = input("Moneda: ")

                if currency == "":
                    print("ERROR: La moneda es obligatoria")

                elif currency not in currencies:
                    print("ERROR: Moneda no valida")

                else:

                    invoice = {
                        "supplier": supplier,
                        "invoice_number": invoice_number,
                        "amount": amount,
                        "currency": currency
                    }

                    with open("output/invoice.json", "w") as file:
                        json.dump(invoice, file, indent=4)

                    print("Factura guardada correctamente")

        except:
            print("ERROR: El importe debe ser numerico")