def validar_factura(invoice):

    errores = []

    proveedores_permitidos = [
        "AMAZON BUSINESS EU S.A.R.L.",
        "IBM",
        "MICROSOFT",
        "SAP"
    ]

    monedas_permitidas = [
        "EUR"
    ]

    supplier = invoice.get("supplier", "").strip()
    invoice_number = invoice.get("invoice_number", "").strip()
    invoice_date = invoice.get("invoice_date", "").strip()
    due_date = invoice.get("due_date", "").strip()
    amount = invoice.get("amount", "").strip()
    currency = invoice.get("currency", "").strip()

    if supplier == "":
        errores.append("Proveedor vacío")
    elif supplier not in proveedores_permitidos:
        errores.append("Proveedor no permitido")

    if invoice_number == "":
        errores.append("Número de factura vacío")

    if invoice_date == "":
        errores.append("Fecha de factura vacía")

    if due_date == "":
        errores.append("Fecha de vencimiento vacía")

    if amount == "":
        errores.append("Importe vacío")

    if currency == "":
        errores.append("Moneda vacía")
    elif currency not in monedas_permitidas:
        errores.append("Moneda no permitida")

    if len(errores) == 0:
        return {
            "estado": "OK",
            "errores": []
        }

    return {
        "estado": "RECHAZADA",
        "errores": errores
    }