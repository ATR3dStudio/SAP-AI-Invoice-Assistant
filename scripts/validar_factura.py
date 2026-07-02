def validar_factura(invoice):

    errores = []

    proveedores_permitidos = [
        "AMAZON BUSINESS EU S.A.R.L.",
        "IBM",
        "MICROSOFT",
        "SAP"
    ]

    monedas_permitidas = [
        "EUR",
        "USD",
        "GBP"
    ]

    if invoice["supplier"] not in proveedores_permitidos:
        errores.append("Proveedor no permitido")

    if invoice["invoice_number"] == "":
        errores.append("Número de factura vacío")

    if invoice["amount"] == "":
        errores.append("Importe vacío")

    if invoice["currency"] not in monedas_permitidas:
        errores.append("Moneda no permitida")

    if len(errores) == 0:
        return {
            "estado": "OK",
            "errores": []
        }

    else:
        return {
            "estado": "RECHAZADA",
            "errores": errores
        }