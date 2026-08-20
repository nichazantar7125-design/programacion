def calcularPromedio(notas):
    suma = 0
    for nota in notas:
        suma = suma + nota
    
    promedio = suma / len(notas)
    return promedio


def contarAprobados(notas):
    aprobadas = 0
    
    for nota in notas:
        if nota > 3:
            aprobadas = aprobadas + 1
    
    return aprobadas


def notaMayor(notas):
    menores = 0
    
    for nota in notas:
        if nota <= 3:
            menores = menores + 1
    
    return menores


def procesar(notas):
    promedio = calcularPromedio(notas)
    aprobadas = contarAprobados(notas)
    reprobadas = notaMayor(notas)

    print("Promedio:", promedio)
    print("Notas aprobadas:", aprobadas)
    print("Notas reprobadas:", reprobadas)


def main():
    print("*** Calculo de nota ***")
    n = int(input("Cuantas notas: "))
    
    notas = []

    for i in range(n):
        nota = float(input("Nota: "))
        notas.append(nota)

    procesar(notas)


main()
