class Estudiante:
    def __init__(self, nombre, materia, nota):
        self.nombre = nombre
        self.materia = materia
        self.nota = nota

    def mostrar(self):
        print("*** Datos Estudiante ***")
        print(f"Nombre  : {self.nombre}")
        print(f"Materia : {self.materia}")
        print(f"Nota    : {self.nota}")
        print(f"Estado  : {self.estado()}")

    def cambiarNota(self, nuevaNota):
        if 0 <= nuevaNota <= 5.0:
            self.nota = nuevaNota

    def estado(self):
        if self.nota >= 3.0:
            return "Aprobó"
        else:
            return "Reprobó"


e1 = Estudiante("Ana", "POO", 4.5)
e2 = Estudiante("Carlos", "POO", 3.2)
e3 = Estudiante("Juan", "POO", 4.2)
e4 = Estudiante("Joana", "POO", 4.8)

e3.cambiarNota(5.0)

e1.mostrar()
e2.mostrar()
e3.mostrar()
e4.mostrar()
