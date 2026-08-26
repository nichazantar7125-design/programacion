def actualizarPromedio(estudiante, promedio):
    if(promedio < 0 or promedio > 5):
        print("ERROR: El promedio debe estar entre 0 y 5")
    else:
        estudiante['promedio'] = promedio

def estado(promedio):
    if promedio >= 3:
        return"Aprobo"
    else:
        return"Reprobo"

def mostrar(estudiante):
    print("Nombre    :", estudiante['nombre'])
    print("Correo    :", estudiante['correo'])
    print("Materia   :", estudiante['materia'])
    print("Semestre  :", estudiante['semestre'])
    print("Promedio  :", estudiante['promedio'])
    print("Estado    :", estado(estudiante['promedio']))

def main():
    print("*** Manejo de entidades ***")
    estudiante = {
        "nombre": "Nicole Chazatar",
        "correo": "nichazantar.7125@unicesmag.edu.co",
        "materia": "POO Grupo B",
        "semestre": "segundo",
        "promedio": 4.1

    }
    actualizarPromedio(estudiante, 98)
    mostrar(estudiante)
main()