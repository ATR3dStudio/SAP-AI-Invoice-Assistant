import json
from validar_factura import validar_factura

with open(
    "test_data/facturas_test.json",
    "r",
    encoding="utf-8"
) as file:

    pruebas = json.load(file)

correctas = 0

print("\n========== LABORATORIO DE PRUEBAS ==========\n")

for prueba in pruebas:

    resultado = validar_factura(prueba["invoice"])

    esperado = prueba["resultado_esperado"]

    obtenido = resultado["estado"]

    if esperado == obtenido:

        print(f"✅ {prueba['nombre']}")

        correctas += 1

    else:

        print(f"❌ {prueba['nombre']}")

        print(f"Esperado: {esperado}")

        print(f"Obtenido: {obtenido}")

print("\n============================================")

print(f"Pruebas superadas: {correctas}")

print(f"Pruebas ejecutadas: {len(pruebas)}")