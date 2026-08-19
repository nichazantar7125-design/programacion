def calcularPromedio(nota1, nota2, nota3):
    return (nota1 + nota2 + nota3) / 3


def determinarEstado(promedio):
    if promedio >= 3:
        return "Aprobó"
    else:
        return "Reprobó"


def main():
    print("*** Notas del estudiante ***")

    nombre = input("Ingresar un nombre: ")
    nota1 = float(input("Ingresar nota 1: "))
    nota2 = float(input("Ingresar nota 2: "))
    nota3 = float(input("Ingresar nota 3: "))

    promedio = calcularPromedio(nota1, nota2, nota3)
    estado = determinarEstado(promedio)

    print(f"Nombre: {nombre}")
    print(f"Nota 1: {nota1}")
    print(f"Nota 2: {nota2}")
    print(f"Nota 3: {nota3}")
    print(f"Promedio: {promedio}")
    print(f"Estado: {estado}")


if __name__ == "__main__":
    main()