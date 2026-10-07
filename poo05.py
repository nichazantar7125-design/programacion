class Persona:
    def __init__(self, nombre, documento, correo):
        self.nombre = nombre
        self.documento = documento
        self.correo = correo

    def saludar(self):
        print("Bienvenido")

    @property
    def mostrar(self):
        return f"{self.documento} | {self.nombre} | {self.correo}"

class Estudiante(Persona):
    def __init__(self, nombre, documento, correo, programa, notas):
        super().__init__(nombre, documento, correo)
        self.programa = programa
        self.notas = notas

    def mostrar(self):
        return f"{super().mostrar} | {self.programa} | {self.notas}"

class Docente(Persona):
    def __init__(self, nombre, documento, correo, asignatura, salario):
        super().__init__(nombre, documento, correo)
        self.asignatura = asignatura
        self.salario = salario

    def mostrar(self):
        return f"{super().mostrar} | {self.asignatura} | {self.salario}"

e = Estudiante("Juan Pablo", 1234, "juan@test.com", "Ingenieria", 4.4)
d = Docente("Juan", 1234, "juan@", "POO", 2500000)
print(e.mostrar())
print(d.mostrar())
