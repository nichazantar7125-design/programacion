def procesar(notas):
    suma = 0
    mayores = 0
    menores = 0
    for nota in notas:
        suma = suma + nota
        if nota > 3:
            mayores = mayores + 1
        else:
            menores = menores + 1
    
    promedio = suma / len(notas)
    print("Promedio: ", promedio)
    print("Notas aprobadas:", mayores)
    print("Notas reprobadas:", menores)


def main():
    print("*** Calculo de nota ***")
    n = int(input("Cuantas notas: "))
    notas = []
    # Captura de datos
    for i in range(n):
        nota = float(input("Nota: "))
        notas.append(nota)

    # Procesamiento de datos
    procesar(notas)

main()
