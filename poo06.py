class Periodo:
    def __init__(self, anio, semestre, nombre):
        self.anio = anio
        self.semestre = semestre
        self.nombre = nombre

class Docente:
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo

class Curso:
    def __init__(self, nombre, docente, periodo):
        self.nombre = nombre
        self.docente = docente
        self.periodo = periodo

    def mostrar(self):
        print(f"Curso: {self.nombre} | Docente: {self.docente.nombre}  ({self.docente.correo}) [{self.periodo.anio} - {self.periodo.semestre}]")

periodo = Periodo(2026, 2, "Periodo B2026")

docente1 = Docente("Ernesto Ruiz", "ernesto.ruiz@gmail.com")
curso1 = Curso("POO", docente1, periodo)
curso1.mostrar()

docente2 = Docente("Juan", "juan@gmail.com")
curso2 = Curso("Programacion", docente2, periodo)
curso2.mostrar()

curso3 = Curso("Fisica", docente2, periodo)
curso3.mostrar()