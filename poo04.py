class Estudiante:
    def __init__(self, codigo, nombre, nota):
        self.__codigo = codigo
        self.__nombre = nombre
        self.__nota = nota

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, nuevoCodigo):
        if(nuevoCodigo >= 0):
            self.__codigo = nuevoCodigo

    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevoNombre):
        if len(nuevoNombre) > 0:
            self.__nombre = nuevoNombre

    @property
    def nota(self):
        return self.__nota
    
    @nota.setter
    def nota(self, nuevaNota):
        if(0 <= nuevaNota <= 5):
            self.__nota = nuevaNota

    def mostrar(self):
        return f"{self.codigo} | {self.nombre} | Nota: {self.nota}"

def mostrarTodo(estudiantes):
    print("*** LISTADO DE ESTUDIANTES ***")
    for e in estudiantes:
        print(e.mostrar())

def buscarEstudiante(estudiantes, codigoBuscar):
    for e in estudiantes:
        if e.codigo == codigoBuscar:
            return e
    return None 

def cambiarNota(estudiantes, codigoBuscar):
    estudiante = buscarEstudiante(estudiantes, codigoBuscar)
    if estudiante is not None:
        nuevaNota = float(input("Nueva Nota: "))
        if nuevaNota < 0.0 or nuevaNota > 5.0:
            return False
        estudiante.nota = nuevaNota
        return True
    return False
    
estudiantes = []
estudiantes.append(Estudiante(101, "Lucas", 4.2))
estudiantes.append(Estudiante(102, "Marcos", 3.2))
estudiantes.append(Estudiante(103, "Juanito", 2.2))
estudiantes.append(Estudiante(104, "Maria", 4.8))

mostrarTodo(estudiantes)

codigo = int(input("Codigo a buscar: "))
estudianteBuscado = buscarEstudiante(estudiantes, codigo)
if estudianteBuscado is not None:
    print(f"ENCONTRADO: {estudianteBuscado.mostrar()}")
    if cambiarNota(estudiantes, codigo):
        print("Nota cambiada con exito")
    else:
        print("No se ha cambiado la nota")
else:
    print("Codigo NO encontrado")

mostrarTodo(estudiantes)
