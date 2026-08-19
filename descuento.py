def descuento(valor, porcentaje):
    return valor * porcentaje / 100

def iva(total):
    return total * 0.19

def main():
    print("*** Valor a pagar ***")
    valor = float(input("Subtotal: "))
    porcentaje = float(input("Descuento (%): "))
    dcto = descuento(valor, porcentaje)
    total = valor - dcto 
    impto = iva(total)
    total = total + impto

    print(f"Descuento: {dcto}")
    print(f"IVA : {impto}")
    print(f"Total a pagar: {total}")

if __name__ == "__main__":
    main()