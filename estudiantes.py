def cambiarNota(estudiante, nota):
    if(nota < 0 or nota > 5):
        print("ERROR: No se puede cambiar la nota")
    else:
        estudiante['nota'] = nota

def buscar(estudiantes, valor):
    for estudiante in estudiantes:
        if estudiante['codigo'] == valor:
            return estudiante
    return None

def mostrar(estudiante):
    print("Codigo    :", estudiante['codigo'])
    print("Nombre    :", estudiante['nombre'])
    print("Nota      :", estudiante['nota'])

def main():
    print("*** Manejo de Estudiantes ***")
    estudiantes = [
        {"codigo": 1, "nombre": "Juan", "nota": 3.2},
        {"codigo": 2, "nombre": "Lucas", "nota": 1.2},
        {"codigo": 3, "nombre": "Marcos", "nota": 2.2},
        {"codigo": 4, "nombre": "Mateo", "nota": 4.2},
        {"codigo": 5, "nombre": "Maria", "nota": 5.0}
    ]

    cod = int(input("Codigo a Buscar: "))
    est= buscar(estudiantes,cod)
    if est is not None:
        mostrar(est)
        nuevaNota = float(input("Nueva nota: "))
        cambiarNota(est, nuevaNota)
        print("**********")
        mostrar(est)
    else:
        print("Codigo no encontrado")

main()