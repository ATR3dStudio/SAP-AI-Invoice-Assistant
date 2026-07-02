vendors = ["Amazon", "Microsoft", "IBM"]

supplier = input("Proveedor: ")

if supplier in vendors:
    print("Proveedor encontrado")
else:
    print("ERROR: Proveedor no existe")