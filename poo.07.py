class Jugador:
    def __init__(self, nombre, anio):
        self.nombre = nombre
        self.anio = anio

    @property
    def mostrar(self):
        return f"{self.nombre} ({self.anio})"

class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.jugadores = []

    def agregar(self, jugador):
        self.jugadores.append(jugador)

    def mostrar(self):
        print(f"***{self.nombre.upper()}***")
        for indice, j in enumerate (self.jugadores, 1):
            print(f"{indice}. {j.mostrar}")

equipo1 = Equipo("Aguilas")
j1 = Jugador("Pablo", 1990)
j2 = Jugador("Marcos", 1995)
j3 = Jugador("Esteban", 2000)
equipo1.agregar(j1)
equipo1.agregar(j2)
equipo1.agregar(j3)
equipo1.mostrar()        