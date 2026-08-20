def calcularPromedio(n1, n2, n3):
    return (n1*0.3)+(n2*0.3)+(n3*0.4)

def determinarEstado(promedio):
    if promedio >= 3.0:
        return "Aprobo"
    else:
        return "Reprobo"

def mostrarDatos(nombre, promedio, estado):
    print("Nombre: ", nombre)
    print("Promedio: ", promedio)
    print("Estado: ", estado)

def main ():
    nombre = input("Nombre: ")
    n1 = float(input("Nota 1: "))
    n2 = float(input("Nota 2: "))
    n3 = float(input("Nota 3: "))
    prom = calcularPromedio(n1,n2,n3)
    est = determinarEstado(prom)
    mostrarDatos(nombre, prom ,est)

main()